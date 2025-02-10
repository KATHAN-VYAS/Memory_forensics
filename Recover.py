#for all jpg files restore

drive = r"\\.\D:"  # Open drive as raw bytes
fileD = open(drive, "rb")
size = 512  # Size of bytes to read
offs = 0  # Offset location
drec = False  # Recovery mode
rcvd = 0  # Recovered file ID

# Read the first chunk of bytes
byte = fileD.read(size)

while byte:
    found = byte.find(b'\xff\xd8\xff\xe0\x00\x10\x4a\x46')
    
    # Corrected comparison operator, use '>= 0'
    if found >= 0:
        drec = True
        print('==== Found JPG at location: ' + str(hex(found + (size * offs))) + ' ====')
        
        # Create a new file for the recovered JPG
        fileN = open(str(rcvd) + '.jpg', "wb")
        fileN.write(byte[found:])
        
        while drec:
            byte = fileD.read(size)
            if not byte:  # End of file check
                break
            
            bfind = byte.find(b'\xff\xd9')
            
            # Corrected comparison operator, use '>= 0'
            if bfind >= 0:
                fileN.write(byte[:bfind + 2])
                print('==== Wrote JPG to location: ' + str(rcvd) + '.jpg ====\n')
                drec = False
                rcvd += 1
                fileN.close()
                
                # Seek to the correct position after finding the JPG end
                fileD.seek((offs + 1) * size)
            else:
                fileN.write(byte)
    byte = fileD.read(size)
    offs += 1

fileD.close()
