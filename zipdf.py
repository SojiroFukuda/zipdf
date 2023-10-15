# merge two pdf files and save it as a new file
# NOTE: you cannot replace the existance file with this method
def pdfmerge(paths: list, savepath: str ):
    """ 
    Merge multiple PDFs into a new single PDF, keeping the originals. 

    Parameters
    ----------
    paths : 1-D list
        A list of filepaths of the target PDFs which you want to merge.
    savepath : str
        String of the filepath where you want to save the merged PDF.
    ----------
    """
    from PyPDF2 import PdfMerger
    merger = PdfMerger()
    for path in paths:
        merger.append(path)
    merger.write(savepath)
    merger.close()

# merge two pdf files and overwrite to path1
# NOTE: original path1 file will disappearoverwrite=True
def overwritePDFmerger(path1: str, path2: str) -> None:
    """ 
    Merge and overwrite two PDF documents.
    WARNING: The first PDF (path1) will be overwritten as the new merged PDF. 
    The second PDF (path2) will remain as it is.

    Parameters
    ----------
    path1 : str
        The main PDF to which you want to merge another PDF. 
    path2 : str
        The PDF which you want to merge to path1. 
    ----------
    """
    import os
    pathlist = [path1,path2]
    pdfmerge(pathlist,path1[0:-len('.pdf')]+'_copy.pdf')
    os.remove(path1)
    os.rename(path1[0:-len('.pdf')]+'_copy.pdf',path1)

# Merge all PDF files in the specified folder path.
def mergePDFsinFolder(folder_path: str, savepathname: str, recursive: bool = True, LOG: bool = False) -> None:
    """ 
    Merge all PDF documents in the specified folder as a new PDF.

    Parameters
    ----------
    folder_path : str
        a path of the directory where multiple PDF documents locate. 
    savepathname : str
        the path of the merged PDF to be saved.
    recursive = True : bool
        Set False if you do not want to include the documents in subfolders
    LOG = False : bool
        Set True if you want to see the number of PDF to be merged.
    ----------
    """
    import glob
    import os
    if recursive: # search in subfolders
        path_list = glob.glob(folder_path+os.sep+'**'+os.sep+'*'+'.pdf',recursive=recursive)
    else: # without seaching subfolders
        path_list = glob.glob(folder_path+os.sep+'*.pdf',recursive=recursive)
    path_list.sort()
    if LOG:
        print('Total PDF files:',len(path_list))
    for i in range(len(path_list)-1):
        if os.path.isfile(savepathname):
            overwritePDFmerger(path1=savepathname,path2=path_list[i+1])
        else:
            pdfmerge([path_list[0],path_list[i+1]],savepathname)
    

# Convert multiple images into a single PDF
def convertImages2pdf(folder_path: str,savename: str,img_format: str = 'all',n: int = 10,recursive: bool = False, LOG: bool = True, sortby='numbering') -> None:
    """ 
    Merge all images in the specified folder as a new PDF.

    Parameters
    ----------
    folder_path : str
        a path of the directory where multiple images locate. 
    savename : str
        the file name of the output PDF which will be saved in the folder_path. 
    img_format : str
        Specify the extension of your images such as '.png, '.webp', or '.JPG'. If you want to merge images regardless of the file extension, then write 'all'. It is set as 'all' by default.
    n : int
        The maximum number of images which are merged at each iteration. The bigger, the faster. However, if the size of your each image is large, the large n can eat memory up easily.
    recursive : bool
        Set False if you do not want to include the documents in subfolders
    LOG : bool
        Set False if you do not want to see the log.
    sortby : str
        sort images in the folder by number in the file name (sortyby='numbering'), or alphabetically (sortby='alphabetical').
    ----------
    """
    
    from PIL import Image # convert images to pdf
    import os # file management
    import glob
    
    # img_format check
    if img_format == 'all':
        img_format = ''
    # Extract img files with the specified format
    if recursive:
        path_list = glob.glob(folder_path+os.sep+'**'+os.sep+'*'+img_format, recursive=recursive)
        path_list = [path for path in path_list if os.path.isfile(path)]
    else:
        files = os.listdir(folder_path) # file names 
        path_list = [] # paths of each img
        for i,file in enumerate(files):
            if img_format in file and os.path.isfile(folder_path+os.sep+file) and '.pdf' in file == False:
                path_list.append(folder_path+os.sep+file) # full path
    # delete pdf if contain
    for path in path_list:
        if '.pdf' in path:
            path_list.remove(path)
    # estimate the iteration 
    num = len(path_list) # number of files
    ite = num // n # number of iteration
    mod = num % n # total number of files in the last iteration
    if LOG:
        print('image files:',num)
    # if there are no img files in the folder, raise an error
    if len(path_list) == 0: # if there are no image files in the folder, raise an error
        raise(ValueError('There is no image file in the specified folder. Double check the img_format and folder_path.'))
    else: # convert detected images into a single PDF
        if sortby == 'numbering':
            import re
            # check if all images have number in the file name
            checker = True
            exceptions = []
            numbers = []
            for name in path_list:
                if re.sub('\D','',name) == '':
                    checker = False
                    exceptions.append(name)
                else:
                    numbers.append(name)
            if checker: # if all images have numbers in the file name
                path_list.sort(key= lambda f: int(re.sub('\D','',f)) ) # sort paths by the numbering 
            else: # if there is any exception
                numbers.sort(key= lambda f: int(re.sub('\D','',f)) ) # sort paths by the numbering
                exceptions.sort()
                path_list = exceptions + numbers 
        elif sortby == 'alphabetical':
            path_list.sort() # sort paths in alphabetical order
        else:
            import warnings
            warnings.warn('unknown sorting method: \'{}\'. possible \'sortby\' option is [\'numbering\', \'alphabetical\'].'.format(sortby),UserWarning)
        for i in range(ite+1):
            start_index = i*n # start index of ith iteration
            if i == ite: # end index of ith iteration
                end_index = num
            else:
                end_index = (i+1)*n
            target_paths = path_list[start_index:end_index] # path lists of ith iteration
            image_list = [] # PIL objects
            if len(target_paths) != 0:
                for path in target_paths:
                    im = Image.open(path) # load image
                    im = im.convert('RGB') # conversion
                    image_list.append(im) # store in a list
                title = savename[0:-len('.pdf')] # file name of output pdf without extension
                # assign a list of images which will be merged with the output PDF
                if len(image_list) < 2:
                    appends = [] 
                else:
                    appends = image_list[1:]
                # if i == 0: # Create first PDF
                if os.path.isfile(folder_path+os.sep+savename): # if the savepath already exist, add the images to the file.
                    image_list[0].save(folder_path+os.sep+title+'_temp.pdf',save_all=True,append_images=appends) # Export PDF
                    overwritePDFmerger(folder_path+os.sep+savename,folder_path+os.sep+title+'_temp.pdf')
                    os.remove(folder_path+os.sep+title+'_temp.pdf')
                else: # if there is no such file, create it
                    image_list[0].save(folder_path+os.sep+savename,save_all=True,append_images=appends) # Export PDF
                
    # log 
    if LOG:
        print('In total, {} {} images are merged.'.format(len(path_list),img_format))
        print('The output pdf is saved as {}'.format(folder_path+os.sep+savename))



# Unzip and convert the images inside into a single PDF
def zip2pdf(filepath,save_folder='',img_format='all',n=10,recursive=True,LOG=False,delete_unzipped=True,sortby='numbering') -> None:
    """ 
    Unzip a zip file in the folder and merge the images inside as a single PDF.

    Parameters
    ----------
    filepath : str
        a path of the zip file. 
    save_folder : str
        a path of the directory where the converted PDFs will be saved
    img_format : str
        Specify the extension of your images such as '.png, '.webp', or '.JPG'. If you want to merge images regardless of the file extension, then write 'all'. It is set as 'all' by default.
    n : int
        The maximum number of images which are merged at each iteration. The bigger, the faster. However, if the size of your each image is large, the large n can eat memory up easily.
    recursive : bool
        Set False if you do not want to include the documents in subfolders
    LOG : bool
        Set False if you do not want to see the log.
    delete_unzipped : bool
        True by default. Set False if you want to keep unzipped files which will be temporalily created in 'savefolder'.
    sortby : str
        sort images in the folder by number in the file name (sortyby='numbering'), or alphabetically (sortby='alphabetical').
    ----------
    """
    import os
    
    folderpath = filepath[:-len(filepath.split(os.sep)[-1])] # folder which contains the zip file
    file = filepath.split(os.sep)[-1] # file name of the zip
    if save_folder == '':
        save_folder = folderpath + os.sep
    if '.zip' in file:
        print(save_folder)
        dir = save_folder+os.sep+file[0:-len('.zip')]
        os.makedirs(dir,exist_ok=True)
        import zipfile
        with zipfile.ZipFile(filepath,'r') as zip_ref:
            zip_ref.extractall(dir) # extract all from the zip file
            convertImages2pdf(dir,file[0:-len('.zip')]+'.pdf',img_format=img_format,LOG=LOG,n=n,recursive=recursive,sortby=sortby) # convert images to a pdf
            # delete extracted files
            if delete_unzipped:
                for img in os.listdir(dir):
                    if os.path.isfile(img):
                        if file[0:-len('.zip')]+'.pdf' in img:
                            pass
                        else:
                            os.remove(dir+os.sep+img)
                if recursive:
                    from glob import glob
                    dirs = []
                    for path in glob(dir+os.sep+'**'+os.sep+'*', recursive=recursive):
                        if os.path.isdir(path):
                            dirs.append(path)
                        elif os.path.isfile(path):
                            if file[0:-len('.zip')]+'.pdf' in path:
                                pass
                            else:
                                os.remove(path)
                    for path in dirs:
                        os.rmdir(path)
    else:
        print('Given path is not a zip file.')


# Unzip all zip files then convert all the images inside into a single PDF
def allzip2pdf(zip_folder,save_folder='',img_format='all',n=10,recursive=True,LOG=False,delete_unzipped=True,sortby='numbering') -> None:
    """ 
    Unzip zip files in the folder and merge the images inside as a single PDF.

    Parameters
    ----------
    zip_folder : str
        a path of the directory where multiple zip files locate. 
    save_folder : str
        a path of the directory where the converted PDFs will be saved. If none, it will be saved in the same folder of the zipfile.
    img_format : str
        Specify the extension of your images such as '.png, '.webp', or '.JPG'. If you want to merge images regardless of the file extension, then write 'all'. It is set as 'all' by default.
    n : int
        The maximum number of images which are merged at each iteration. The bigger, the faster. However, if the size of your each image is large, the large n can eat memory up easily.
    recursive : bool
        Set False if you do not want to include the documents in subfolders
    LOG : bool
        Set False if you do not want to see the log.
    sortby : str
        sort images in the folder by number in the file name (sortyby='numbering'), or alphabetically (sortby='alphabetical').
    ----------
    """
    import os
    from tqdm import tqdm # progress bar
    
    files = os.listdir(zip_folder)
    zips = [val for val in files if ('.zip' in val) and (val[0] != '.') ]
    if LOG:
        print(str(len(zips)),'zip files are found.')
        print([val for val in files if '.zip' in val])
        for file in zips:
            zip2pdf(zip_folder+os.sep+file,save_folder=save_folder,img_format=img_format,n=n,recursive=recursive,LOG=LOG,delete_unzipped=delete_unzipped,sortby=sortby)
        print('done')
    else:
        pbar = tqdm(zips)
        for file in pbar:
            pbar.set_description(f"Processing {file}")
            zip2pdf(zip_folder+os.sep+file,save_folder=save_folder,img_format=img_format,n=n,recursive=recursive,LOG=LOG,delete_unzipped=delete_unzipped,sortby=sortby)