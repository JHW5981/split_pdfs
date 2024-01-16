import argparse
from pathlib import Path
import fitz

def get_arguments():

    parser = argparse.ArgumentParser(description='Split Arguments')
    
    parser.add_argument('--pdf_path', type=str, required=True, help='Input file path')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory path')

    args = parser.parse_args()

    return args

def main():
    args = get_arguments()
    input_path = Path(args.pdf_path)
    output_dir = Path(args.output_dir)

    doc = fitz.open(input_path)
    for pag_num in range(doc.page_count):
        page = doc[pag_num]
        text = page.get_text("words")
        # find the central point coordinate of RT[min] and Calc.MW
        x1 = (343.3+368.3)/2
        y1 = (109.8+121.2)/2

        x2 = (646.3+688.0)/2
        y2 = (109.1+120.5)/2

        rt = ""
        calc = ""

        for i in text:
            m0 = i[0]
            n0 = i[1]
            m1 = i[2]
            n1 = i[3]
            # extract the proper position data
            if x1 > m0 and x1 < m1 and y1 > n0 and y1 < n1:
                rt = i[4]
            elif x2 > m0 and x2 < m1 and y2 > n0 and y2 < n1:
                calc = i[4]
        doc1 = fitz.open(input_path)
        doc1.select([pag_num])
        if rt != '' and calc != '':
            doc1.save(output_dir / f"{pag_num+1}-{rt}-{calc}.pdf", deflate =True, garbage=3)
        elif rt == '' and calc != '':
            doc1.save(output_dir / f"{pag_num+1}-Nan-{calc}.pdf", deflate =True, garbage=3)
        elif rt != '' and calc == '':
            doc1.save(output_dir / f"{pag_num+1}-{rt}-Nan.pdf", deflate =True, garbage=3)
        else:
            doc1.save(output_dir / f"{pag_num+1}-Nan-Nan.pdf", deflate =True, garbage=3)

if __name__ == '__main__':
    main()