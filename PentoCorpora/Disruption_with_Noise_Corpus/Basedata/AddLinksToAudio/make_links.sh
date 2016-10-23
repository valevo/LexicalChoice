#!/bin/tcsh -f

set basedir = "../../../../Data/Pentomino_Task"

set outdir = "."

ln -s $basedir/NoNoise/2006-11-23_run1/20061123_pento_nonoise.aif $outdir
ln -s $basedir/NoNoise/2007-02-01_run1/20070201_run1pento_nonoise.aif $outdir
ln -s $basedir/NoNoise/2007-02-01_run4/20070201_run4pento_nonoise.aif $outdir
ln -s $basedir/NoNoise/2007-01-24_run1/20070124_run1pento_nonoise.aif $outdir
ln -s $basedir/NoNoise/2007-02-01_run3/20070201_run3pento_nonoise.aif $outdir
ln -s $basedir/Noise/2006-11-17_run1/20061117_run1pento_noise.aif $outdir
ln -s $basedir/Noise/2007-01-17_run1/20070117_run1pento_noise.aif $outdir
ln -s $basedir/Noise/2007-01-31_run2/20070131_run2pento_noise.aif $outdir
ln -s $basedir/Noise/2006-11-17_run2/20061117_run2pento_noise.aif $outdir
ln -s $basedir/Noise/2007-01-31_run1/20070131_run1pento_noise.aif $outdir
ln -s $basedir/Noise/2007-01-31_run3/20070131_run3pento_noise.aif $outdir


