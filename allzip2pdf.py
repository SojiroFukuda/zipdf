import zipdf
import argparse

if __name__ == '__main__':
    # initiate parser
    parser = argparse.ArgumentParser(description='Convert all zip files into PDF files.')
    
    # add arguments
    parser.add_argument('zipfolder',help='Folderpath where your zip files are located.',nargs=1) # folder path
    parser.add_argument('--savefolder',help='Folderpath where the created PDFs will be saved.',type=str, default='') # save folder
    parser.add_argument('--img_format',help='Specify extension of image files you want to merge. If you want to merge all images files regardless of their extensions, set it as \'all\'. It is \'all\' by default',type=str, default='all') # extension of the img files
    parser.add_argument('--n',help='number of image files you to process at each iteration. Large n may result in memory shortage. 50 by default.', type=int,default=50)
    parser.add_argument('--recursive',help='True by default. Set it False if you want to ignore any subfolders in the zip file.',type=bool,default=True)
    parser.add_argument('--sortby',help='sort images in the folder by number in the file name (sortyby=\'numbering\'), or alphabetically (sortby=\'alphabetical\')',type=str,default='numbering')
    parser.add_argument('--log',help='show logs. False by default.',type=bool,default=False)
    # receive args
    args = parser.parse_args()
    
    # main
    if args.savefolder == '':
        args.savefolder = args.zipfolder[0]
    zipdf.allzip2pdf(
        args.zipfolder[0],
        args.savefolder,
        img_format=args.img_format,
        n=args.n,
        recursive=args.recursive,
        sortby=args.sortby,
        LOG=args.log
    )
