from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='tcp-ip-poker',
    version='0.0.1',
    description='A TCP/IP socket server that hosts poker game',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/karhu12/TCPIPoker',
    author='Riku Kaipainen',
    author_email='shylessfly@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Anyone',
        'Topic :: Entertainment',
        'License :: OSI Approved :: GNU General Public License',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='tcp/ip socket, poker, entertainment',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.8',
    install_requires=[],
    extras_require={},
    package_data={},
    entry_points={}
)