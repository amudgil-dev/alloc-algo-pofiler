from app.utils.util import Util  

def example_generate_filename():

    prefix = "Distribution"
    ext = ".txt"
    file_name = Util.generate_filename(prefix,ext)
    print(f"filename for {prefix} and {ext} = {file_name}")
            


example_generate_filename()