from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
import subprocess
import oe.lsb

class VirglTest(OERuntimeTestCase):

    @OETestDepends(['ssh.SSHTest.test_ssh'])
    def test_kernel_driver(self):
        status, output = self.target.run('dmesg|grep virgl')
        self.assertEqual(status, 0, "Checking for virgl driver in dmesg returned non-zero: %d\n%s" % (status, output))
        self.assertIn("virgl 3d acceleration enabled", output, "virgl acceleration seems to be disabled:\n%s" %(output))

    @OETestDepends(['virgl.VirglTest.test_kernel_driver'])
    def test_kmscube(self):

        distro = oe.lsb.distro_identifier()
        if distro and distro == 'centos-7':
            self.skipTest('kmscube is not working when centos 7 is the host OS')

        status, output = self.target.run('kmscube', timeout=30)
        self.assertEqual(status, 0, "kmscube exited with non-zero status %d and output:\n%s" %(status, output))
        self.assertIn('renderer: "virgl"', output, "kmscube does not seem to use virgl:\n%s" %(output))
