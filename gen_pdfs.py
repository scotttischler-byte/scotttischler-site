import os, glob, asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.abspath(__file__))
PDFDIR=os.path.join(ROOT,"articles","pdf")
files=sorted(glob.glob(os.path.join(PDFDIR,"*.print.html")))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page()
        n=0
        for f in files:
            slug=os.path.basename(f)[:-len(".print.html")]
            out=os.path.join(PDFDIR,slug+".pdf")
            await pg.goto("file://"+f)
            await pg.wait_for_timeout(400)
            await pg.pdf(path=out,format="Letter",print_background=True,
                margin={"top":"0","bottom":"0","left":"0","right":"0"})
            n+=1
        await b.close()
        print("generated",n,"pdfs")
asyncio.run(main())
