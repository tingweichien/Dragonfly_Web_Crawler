import chromedriver_autoinstaller

def check_chromedriver():
    # Check if the current version of chromedriver exists
    # and if it doesn't exist, download it automatically,
    # then add chromedriver to path
    chromedriver_autoinstaller.install(True)