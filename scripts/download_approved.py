#!/usr/bin/env python3
"""
Download approved models where automation is practical.
- GitHub: tries to download model files from public repos/paths using the GitHub contents API.
- Thingiverse: downloads files with --thingiverse-token.
- Printables/MakerWorld: creates folders, writes SOURCE.md, opens browser tabs for manual download.
"""
from __future__ import annotations
import argparse, csv, os, re, sys, time, webbrowser
from pathlib import Path
from urllib.parse import urlparse, unquote
import requests

SOURCE_EXTS=(".step",".stp",".scad",".f3d",".fcstd",".sldprt")
MODEL_EXTS=(".stl",".3mf",".obj")
EXTS=SOURCE_EXTS+MODEL_EXTS
UA="offgrid-stl-downloader/0.1"

def safe(s:str)->str:
    s=re.sub(r"[^A-Za-z0-9._ -]+","_",s or "")
    s=re.sub(r"\s+","_",s.strip())
    return s[:90] or "model"

def source_md(row):
    return f"""# {row.get('title') or row.get('target_item')}

- Target: {row.get('target_item','')}
- Category: {row.get('category','')}
- Source: {row.get('source','')}
- URL: {row.get('url','')}
- Review notes: {row.get('review_notes','')}
- Score: {row.get('score','')}

## Safety
Verify dimensions, material, and license before redistribution. Do not use printed parts for pressurized potable water, mains voltage, load-bearing trailer/vehicle hardware, or other critical safety functions.
"""

def folder_for(row,outbase):
    return Path(outbase)/safe(row.get('category','Uncategorized'))/safe(row.get('target_item','target'))/safe(row.get('title') or row.get('candidate_id','candidate'))

def download_url(url, dest):
    r=requests.get(url,headers={"User-Agent":UA},timeout=60)
    r.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(r.content)
    return len(r.content)

def parse_github(url):
    p=urlparse(url)
    if "raw.githubusercontent.com" in p.netloc:
        return {"raw":url}
    if "github.com" not in p.netloc: return None
    parts=[x for x in p.path.strip('/').split('/') if x]
    if len(parts)<2: return None
    owner,repo=parts[0],parts[1]
    branch="main"; subpath=""
    if len(parts)>=5 and parts[2] in ("tree","blob"):
        branch=parts[3]; subpath="/".join(parts[4:])
        if parts[2]=="blob":
            raw=f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{subpath}"
            return {"raw":raw, "owner":owner, "repo":repo, "branch":branch, "path":subpath}
    return {"owner":owner,"repo":repo,"branch":branch,"path":subpath}

def github_contents(owner,repo,path,branch):
    api=f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    r=requests.get(api,headers={"User-Agent":UA},params={"ref":branch},timeout=30)
    if r.status_code==404 and branch=="main":
        return github_contents(owner,repo,path,"master")
    r.raise_for_status()
    return r.json(), branch

def download_github(url, dest):
    info=parse_github(url)
    if not info: return 0
    files_dir=dest/"files"; files_dir.mkdir(parents=True, exist_ok=True)
    count=0
    if "raw" in info and any(info["raw"].lower().split('?')[0].endswith(e) for e in EXTS):
        name=Path(urlparse(info["raw"]).path).name
        download_url(info["raw"], files_dir/safe(unquote(name)))
        return 1
    owner,repo,branch,path=info["owner"],info["repo"],info.get("branch","main"),info.get("path","")
    try:
        data, branch = github_contents(owner,repo,path,branch)
    except Exception as e:
        print(f"  GitHub API failed: {e}")
        return 0
    stack=data if isinstance(data,list) else [data]
    while stack:
        item=stack.pop()
        if item.get("type")=="dir":
            try:
                children,_=github_contents(owner,repo,item.get("path",""),branch)
                if isinstance(children,list): stack.extend(children)
            except Exception as e:
                print(f"  Could not list {item.get('path')}: {e}")
        elif item.get("type")=="file":
            name=item.get("name","")
            if name.lower().endswith(EXTS) and item.get("download_url"):
                try:
                    size=download_url(item["download_url"], files_dir/safe(name))
                    print(f"  downloaded {name} ({size} bytes)")
                    count+=1
                except Exception as e:
                    print(f"  failed {name}: {e}")
    return count

def thingiverse_id(url):
    m=re.search(r"thing:(\d+)",url)
    if m: return m.group(1)
    m=re.search(r"/things/(\d+)",url)
    return m.group(1) if m else ""

def thingiverse_get(path,token):
    r=requests.get("https://api.thingiverse.com"+path,headers={"User-Agent":UA,"Authorization":f"Bearer {token}"},timeout=30)
    r.raise_for_status(); return r.json()

def ext_priority(name, prefer_source=False):
    n=name.lower()
    order = list(SOURCE_EXTS)+list(MODEL_EXTS) if prefer_source else list(MODEL_EXTS)+list(SOURCE_EXTS)
    for i,e in enumerate(order):
        if n.endswith(e): return i
    return 999

def download_thingiverse(url, dest, token, prefer_source=False):
    tid=thingiverse_id(url)
    if not tid:
        print("  no thing ID found") ; return 0
    files=thingiverse_get(f"/things/{tid}/files",token)
    files_dir=dest/"files"; files_dir.mkdir(parents=True, exist_ok=True)
    count=0
    files = sorted(files, key=lambda f: ext_priority(f.get("name") or "", prefer_source=prefer_source))
    for f in files:
        name=f.get("name") or "file"
        dl=f.get("direct_url") or f.get("download_url")
        if not dl: continue
        if not name.lower().endswith(EXTS): continue
        try:
            size=download_url(dl, files_dir/safe(name))
            print(f"  downloaded {name} ({size} bytes)")
            count+=1
            time.sleep(0.5)
        except Exception as e:
            print(f"  failed {name}: {e}")
    return count

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--approved", default="manifests/approved_models.csv")
    ap.add_argument("--out", default="models")
    ap.add_argument("--thingiverse-token", default=os.environ.get("THINGIVERSE_TOKEN",""))
    ap.add_argument("--open-manual", action="store_true", help="Open Printables/MakerWorld pages in browser")
    ap.add_argument("--prefer-source", action="store_true", help="Prioritize STEP/STP/SCAD/F3D/FCStd files first when downloading")
    args=ap.parse_args()
    with open(args.approved,newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    total_files=0
    for row in rows:
        url=row.get('url',''); src=row.get('source','')
        dest=folder_for(row,args.out); dest.mkdir(parents=True, exist_ok=True)
        (dest/"SOURCE.md").write_text(source_md(row),encoding='utf-8')
        print(f"\n{row.get('target_item')} -> {dest}")
        if src=="github":
            total_files += download_github(url,dest)
        elif src=="thingiverse":
            if args.thingiverse_token:
                total_files += download_thingiverse(url,dest,args.thingiverse_token,args.prefer_source)
            else:
                print("  skipped Thingiverse: pass --thingiverse-token or set THINGIVERSE_TOKEN")
        else:
            print("  manual source: folder + SOURCE.md created")
            if args.open_manual:
                webbrowser.open(url)
                time.sleep(1)
    print(f"\nDone. Downloaded {total_files} model files automatically.")
    print("Run: python3 scripts/audit_downloads.py --models models --out manifests/download_audit.csv")
if __name__=='__main__': main()
