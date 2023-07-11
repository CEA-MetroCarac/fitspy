from setuptools import setup, find_packages

setup(
    name="fitspy",
    version='2023.3',
    license='GPL v3',
    include_package_data=False,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "lmfit",
        "pywin32; platform_system == 'Windows'",
    ],
    packages=find_packages(),

    description="Fitspy (A generic tool to fit spectra in python)",

    url="https://github.com/CEA-MetroCarac/fitspy",
    author_email="patrick.quemere@cea.fr",
    author="Patrick Quéméré",
    keywords="Fitspy, fit, spectra, spectrum, map, 1D, 2D, decomposition, "
             "Gaussian, Lorentzian, Pseudovoigt, GUI",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: Console',
    ],

    entry_points={
        'gui_scripts': [
            'fitspy = fitspy.app.gui:fitspy_launcher',
        ]
    }

)
