#!/bin/sh

echo "Building common lib..."
cd common/libs
python3 ../../lib_build.py
cd zip
zip -x .git -r ../python3.zip .
cd ../../
cp libs/python3.zip ../client/libs/
cp libs/python3.zip ../server/libs/
echo "Building client lib..."
cd ../client/libs
python3 ../../lib_build.py
cd zip
zip -x .git -r ../python3.zip .
cd ../../
echo "Building server lib..."
cd ../server/libs
python3 ../../lib_build.py
cd zip
zip -x .git -r ../python3.zip .
