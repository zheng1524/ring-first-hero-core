"""Serve only visualization/, test a fresh headless browser, then stop our server."""
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
import json
import re

ROOT=Path(__file__).resolve().parents[1]

def main():
    data=ROOT/'.local_data/browser';data.mkdir(parents=True,exist_ok=True)
    serverlog=(data/'server.log').open('w')
    server=subprocess.Popen([sys.executable,'-m','http.server','8765','--bind','127.0.0.1','--directory',str(ROOT/'visualization')],stdout=serverlog,stderr=serverlog)
    try:
        for _ in range(50):
            try:
                text=urllib.request.urlopen('http://127.0.0.1:8765/',timeout=1).read().decode();break
            except Exception:
                if server.poll() is not None:raise RuntimeError('Our local HTTP server could not start')
                time.sleep(.1)
        else:raise RuntimeError('HTTP server timeout')
        refs=re.findall(r'(?:src|href)="([^"#]+)"',text)
        for url in refs:
            if not url.startswith(('https:','http:')):
                with urllib.request.urlopen('http://127.0.0.1:8765/'+url,timeout=10)as r:assert r.status==200
        cmd=['/usr/bin/google-chrome','--headless=new','--disable-dev-shm-usage','--no-first-run','--no-default-browser-check','--user-data-dir='+str(data/'profile'),'--use-angle=swiftshader','--enable-unsafe-swiftshader','--window-size=1440,1100','--virtual-time-budget=18000','--dump-dom','--screenshot='+str(data/'gallery.png'),'http://127.0.0.1:8765/']
        run=subprocess.run(cmd,capture_output=True,timeout=60)
        (data/'dom.html').write_bytes(run.stdout);(data/'chrome.stderr.txt').write_bytes(run.stderr)
        dom=run.stdout.decode(errors='replace')
        ready='data-load-status="ready"'in dom
        second=subprocess.run(cmd[:-1]+['http://127.0.0.1:8765/?scene=G03_native_sources'],capture_output=True,timeout=60)
        dom2=second.stdout.decode(errors='replace');(data/'G03_dom.html').write_bytes(second.stdout)
        result=dict(HTTP_internal_resources=len([x for x in refs if not x.startswith(('https:','http:'))]),browser_exit_code=run.returncode,GLB_loaded=ready,canvas_present='<canvas'in dom,source_checkbox_present='data-source='in dom,G03_GLB_loaded='data-load-status="ready"'in dom2,G03_source_checkboxes=len(re.findall(r'data-source="[^"]+"',dom2)),network_required_for_gallery=False,screenshot_exists=(data/'gallery.png').exists())
        (ROOT/'validation/BROWSER_SMOKE.json').write_text(json.dumps(result,indent=2))
        print(result)
        if run.returncode or not ready or not result['G03_GLB_loaded'] or result['G03_source_checkboxes']!=2:raise RuntimeError('Browser smoke failed; see ignored .local_data/browser logs')
    finally:
        server.terminate();server.wait(timeout=10);serverlog.close()

if __name__=='__main__':main()
