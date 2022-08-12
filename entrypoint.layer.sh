#!/bin/bash

# Setup defined in .docker.env

# Install perl
curl $PERL_URL | tar xz
cd perl-*
./Configure -de -Dman1dir=none -Dman3dir=none -Dprefix=$BIN_PATH
make
make install

# Install exiftool
curl $EXIFTOOL_URL | tar xz
mkdir -p $BIN_PATH/bin/lib
cp ./Image-ExifTool*/exiftool $BIN_PATH/bin/
cp -r ./Image-ExifTool*/lib/* $BIN_PATH/bin/lib/
sed -i "1 s|^.*$|#!$BIN_PATH/bin/perl -w|" $BIN_PATH/bin/exiftool

# Copy files to shared path
cd $BIN_PATH
zip -FSr $LAYER_PATH/exiftool.zip bin/perl lib/perl*/* bin/exiftool bin/lib/*
