#sphinx-apidoc --file-insertion-enabled -f -o source ../src tests conf conf.py modules
# Clear previous run
rm -rf source

# Generate docs. Exclusions are handled by conftest.py
sphinx-apidoc --separate --remove-old --module-first -f -o source '../src' 'source/**metric.py'

# Build HTML
make html

# Copy to final location
rm -rf html
cp -a _build/html html