from gausstrajlib import errors
import math 
import traceback
class Writer():
    
    def __init__(self):
         pass
    
    def __write_to_gjf_(self, trajectory, param, point = 0):
        pass

    def __write_to_gjfs__(self, datafile, param,  point = 0):
        i = 0 

        chk_index = 0

        for line in param:
            if ('%chk' in line):
                break
                
            else:
                 chk_index += 1

        for trajectory in datafile.trajectories: #write each trajectory the seperate xyz files for organiziation
            cur_traj_vel = trajectory.atom_vel if len(trajectory.atom_vel) >= trajectory.atomicity else []
            cur_traj_xyz = trajectory.atom_xyz
            cur_traj_sym = trajectory.atom_symbols
            num_atoms = trajectory.atomicity
            charge = trajectory.charge
            multiplicity = trajectory.mult
            bonding = 0

            basename = datafile.name.split('.')[0]
            outname = f"{basename}_T{i+1}.gjf"
            
            try:    
                with open(outname, 'w') as out:
                    param[chk_index] = f"%chk={basename}_T{i+1}.chk\n"

                    for line in param:
                        out.write(line)
                    out.write('\n\n')
                    out.write(f"{charge} {multiplicity}\n")
                    for j in range(len(cur_traj_sym[(point * num_atoms):((point+1)*num_atoms)])):
                        out.write(f"\t{cur_traj_sym[j]}\t")
                        current_xyz = cur_traj_xyz[j]
                        for k in current_xyz:
                            out.write(f"{k}\t")
                        out.write('\n')
                    out.write(f"\n\n{bonding}\n\n")
                    for j in range(len(cur_traj_vel[(point * num_atoms):((point+1)*num_atoms)])):
                        current_vel = cur_traj_vel[j]
                        x, y, z = current_vel
                        out.write(f"\t{x}\t\t{y}\t\t{z}\n")        
                    #for j in range(len)
            except Exception as e:
                print(f"Error writing to {outname}")
                print(e)
                traceback.print_exc(e)
            else:
                print(f"Successfully written to {outname}")
                i+=1


    def __write_to_xyz__(self, outname: str, trajectory, grad = True, low_e = float('-inf'), high_e = float('inf')): #function internal to class for writing xyz format for sGDML
                    
                    try:
                        #pull data into easier to access local lists
                        a_s = trajectory.atom_symbols
                        a_xyz = trajectory.atom_xyz
                        a_f = trajectory.atom_forces
                        s_e = trajectory.pot_energy
                        
                        #define attributes important to indexing these lists in the writing steps to come
                        num_atoms = trajectory.atomicity
                        num_xyz_sets = len(a_xyz)
                        num_energies = len(s_e)
                        num_steps = int(((len(a_s)/num_atoms)))

                        if num_atoms == 0:
                            print(num_atoms)
                            print("Null")
                            raise errors.NullWriteError()

                        if (num_energies != num_xyz_sets/num_atoms):
                            print(num_energies)
                            print(num_xyz_sets)
                            print(a_xyz[0:6])
                            print(a_xyz[6:12])
                            print(a_xyz[-6:])
                            print(num_atoms)
                            raise errors.NullWriteError()
                        
                        with open(outname, 'w') as xyz:
                        
                            for j in range(num_xyz_sets):
                        
                                index = int(math.floor(j/num_atoms))
                        
                                if(s_e[index] > low_e and s_e[index] < high_e): #Energy cutoff for reactants in this range
                                    if(j%num_atoms == 0):
                        
                                        step = int(j/num_atoms)
                                        xyz.write(f"{num_atoms}\n") 
                        
                                        if(s_e):
                                            xyz.write(f"{s_e[step]}\n")
                                
                                    symbol = a_s[j]

                                    current_xyz = a_xyz[j] #Format and convert xyz coordinates 
                                    current_forces = a_f[j] #Format and convert force/gradient values 
                                    
                                    coordinates = "\t".join(f"\t{coord:15.12f}" for coord in current_xyz)
                                    forces = "\t".join(f"\t{force:15.12f}" for force in current_forces) if grad else ""
                                    xyz.write(f"{symbol}\t{coordinates}\t{forces}\n")
                        
                        print(f"Success writing to file {outname}")

                    except Exception as e:
                        print(f"An error occurred: {e}")
                        traceback.print_exception(e)


    def __write_to_xyzs__(self, outname: str, trajectory, grad = True, low_e = float('-inf'), high_e = float('inf')):
         pass

    def write(self, output, trajectory, grad = True, low_e = float('-inf'), high_e = float('inf'),):
        self.__write_to_xyz__(output, trajectory, grad = grad, low_e = low_e, high_e = high_e)

