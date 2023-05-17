# Import the required Module
import tabula
name = "m.pdf"
p = 57
# Read a PDF File
m = tabula.read_pdf(name, pages=p)
df = m[0]
# convert PDF into CSV
tabula.convert_into(name, "out.csv", output_format="csv", pages=p)
print(df)