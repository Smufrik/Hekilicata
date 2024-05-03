talents = [18427, 18428, 18429, 13852, 84652, 84653, 84654, 79123, 79125, 13877, 31124, 31126, 31228, 31229, 31230, 14177, 35541, 35550, 35551, 14162, 14163, 14164, 51664, 51665, 51667, 31380, 31382, 31383, 30902, 30903, 30904, 30905, 30906, 51625, 51626, 79121, 79122, 13713, 13853, 13854, 14082, 14083, 13981, 14066, 79150, 79151, 79152, 31211, 31212, 31213, 58414, 58415, 51632, 91023, 13960, 13961, 13962, 30894, 30895, 16511, 51698, 51700, 51701, 14079, 14080, 84661, 14168, 14169, 13741, 13793, 13754, 13867, 14174, 14175, 14176, 14113, 14114, 14115, 14116, 14117, 79007, 79008, 13732, 13863, 79004, 14165, 14166, 13743, 13875, 13976, 13979, 51690, 14128, 14132, 14135, 13712, 13788, 13789, 14138, 14139, 14140, 14141, 14142, 31223, 58410, 14158, 14159, 1329, 31130, 31131, 13975, 14062, 14057, 14072, 79141, 58426, 13705, 13832, 13843, 14183, 14185, 51685, 51686, 51687, 51688, 51689, 13733, 13865, 13866, 31244, 31245, 31208, 31209, 79077, 79079, 14179, 58422, 58423, 14144, 14148, 79095, 79096, 84617, 14251, 14156, 14160, 14161, 79146, 79147, 51682, 58413, 14186, 14190, 14171, 14172, 13983, 14070, 14071, 51713, 36554, 31220, 51708, 51709, 51710, 32601, 5952, 51679, 51627, 51628, 51629, 51672, 51674, 79140, 79133, 79134, 14983, 16513, 16514, 16515, 61329, 51692, 51696, 30919, 30920]

with open('constants.lua', 'r') as file:
    lines = file.readlines()

found_talents = []

for talent in talents:
    for line in lines:
        if str(talent) in line:
            # Extract the number inside the brackets
            start = line.find('[')
            end = line.find(']')
            if start != -1 and end != -1:
                number = line[start+1:end]

                # Extract the talent IDs
                start = line.find('{')
                end = line.find('}')
                if start != -1 and end != -1:
                    ids = line[start+1:end].split(',')

                    # Remove any whitespace from the IDs
                    ids = [id.strip() for id in ids]

                    # Save the found talent and break the inner loop
                    found_talents.append((number, ids))
                    break

# Print all found talents in the specified format
for talent in found_talents:
    number, ids = talent
    print("{  " + str(number) + ",  " + str(len(ids)) + ", " + ", ".join(ids) + ", },")