
import mpi4py.MPI as mpi
from comsyl.utils.Logger import logAll, log
from comsyl.parallel.utils import isMaster, barrier
from socket import gethostname
from comsyl.parallel.DistributionPlan import DistributionPlan
import os

if isMaster():
    print("Hello from master")

if isMaster():
    if not os.path.exists("tmp"):
        os.mkdir("tmp")


logAll("Using LogAll")
log("Using Log")

s_id = str(mpi.COMM_WORLD.Get_rank()) + "_" + gethostname()

print("s_id: ",s_id)
print("str(mpi.COMM_WORLD.Get_rank()): ",str(mpi.COMM_WORLD.Get_rank()))

number_modes = 1000
distribution_plan = DistributionPlan(mpi.COMM_WORLD, n_rows=number_modes, n_columns=1)
print(distribution_plan)


f = open("./tmp/TMP%s_in"%s_id,'w')
f.write(">>>>>>>>>")
f.close
