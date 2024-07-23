import reader
import writer 
filename = "BOMD-TS_T3.log"

rd = reader.Reader()
ts= rd.read_log(filename)
print(ts)
wr = writer.Writer()
for t in ts:
    print(len(t.atom_vel))
    print(t.atomicity)
    wr.__write_to_xyz__(t.name.split('.')[0]+'.xyz', t)
