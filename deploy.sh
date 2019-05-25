#!/bin/sh

echo "Building common lib..."
cd common/libs
python ../../lib_build.py
cd zip
zip -r ../python3.zip .
cd ../../
cp libs/python3.zip ../client/libs/
cp libs/python3.zip ../server/libs/
echo "Building client lib..."
cd ../client/libs
python ../../lib_build.py
cd zip
zip -r ../python3.zip .
