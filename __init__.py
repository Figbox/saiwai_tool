from fastapi import APIRouter, Body, Depends, UploadFile, File
from starlette.responses import FileResponse

from app.core.module_class import ApiModule
from app.core.package_manager import PackageManager
from app.modules.saiwai_tool import crud


class SaiwaiTool(ApiModule):
    def _register_api_bp(self, bp: APIRouter):
        @bp.post('/init')
        def init():
            PackageManager.install_package(['beautifulsoup4'], 'bs4')
            PackageManager.install_package(['pdfplumber'])

        @bp.post('/upload_html2', summary='二番目のHTMLをアップロードしてください')
        def upload_html2(file: bytes = File(...)):
            try:
                with open(self.get_module_directory() + "/2.html", "wb") as f:
                    f.write(file)
            except:
                return "fail"
            return "succ"

        @bp.post('/upload_html3', summary='三番目のHTMLをアップロードしてください')
        def upload_html3(file: bytes = File(...)):
            try:
                with open(self.get_module_directory() + "/3.html", "wb") as f:
                    f.write(file)
            except:
                return "fail"
            return "succ"

        @bp.post('/upload_pdf', summary='PDFファイルをアップロード')
        def upload_pdf(file: bytes = File(...)):
            try:
                with open(self.get_module_directory() + "/saiwai.pdf", "wb") as f:
                    f.write(file)
            except:
                return "fail"
            return "succ"

        @bp.post('/analysis_get_json', summary='分析してjsonファイルを獲得')
        def analysis_and_get_json():
            path = crud.dump_json_from_html(self.get_module_directory())
            return FileResponse(path, media_type='application/json', filename='data.json')

    def _get_tag(self) -> str:
        return 'saiwai_tool'

    def get_module_name(self) -> str:
        return 'saiwai_tool'


saiwai_tool = SaiwaiTool()
