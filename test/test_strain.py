import py4DSTEM
from py4DSTEM import StrainMap
from os.path import join
from numpy import zeros


# TODO add BVs file to test suite with calibration, remove disk detection here

# set filepath
path = join(py4DSTEM._TESTPATH,"strain/downsample_Si_SiGe_analysis_braggdisks_cal.h5")



class TestStrainMap:

    # setup/teardown
    def setup_class(cls):

        # Read braggpeaks
        # origin is calibrated
        cls.braggpeaks = py4DSTEM.io.read( path )


    # tests

    def test_strainmap_instantiation(self):

        strainmap = StrainMap(
            braggvectors = self.braggpeaks,
        )

        assert(isinstance(strainmap, StrainMap))


