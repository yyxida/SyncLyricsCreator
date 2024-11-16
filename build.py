import PyInstaller.__main__

if __name__ == '__main__':
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--clean',
        '--icon',
        'refresh_arrows_14418.ico',  # https://icon-icons.com/download/13695/ICO/256/
        '--add-data',
        'refresh_arrows_14418.ico;.',
    ])
