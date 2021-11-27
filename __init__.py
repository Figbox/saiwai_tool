from fastapi import APIRouter, Body, Depends, UploadFile, File

from app.core.module_class import ApiModule


class SaiwaiTool(ApiModule):
    def _register_api_bp(self, bp: APIRouter):
        @bp.get('/description')
        def description():
            return 'this is a sample module_manager description,' \
                   ' this sample will tell you how to' \
                   ' create a module_manager for Figbox'

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

        @bp.post('/analysis', summary='分析')
        def analysis(s: str):
            return s

    def _get_tag(self) -> str:
        return 'saiwai_tool'

    def get_module_name(self) -> str:
        return 'saiwai_tool'


saiwai_tool = SaiwaiTool()
