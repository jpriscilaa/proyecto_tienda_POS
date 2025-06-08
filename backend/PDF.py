from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0,10,"Tabla de datos", 0,1,"C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
                
        self.cell(0,10,f"Pagina{self.page_no()}", 0,0,"C")


    pass