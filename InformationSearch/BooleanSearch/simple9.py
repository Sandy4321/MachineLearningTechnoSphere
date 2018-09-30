def compress(data, fout):
	residuals = [data[i] for i in range(len(data))]
	residuals[1:] = [residuals[i] - residuals[i - 1] for i in range(1, len(data))]

	# print('residuals', residuals)

	i = 0
	l = 0
	while i < len(data):
		if canPack(residuals, i, 1, 28):
			pack28(residuals, i, fout)
			i += 28
		elif canPack(residuals, i, 2, 14):
			pack14(residuals, i, fout)
			i += 14
		elif canPack(residuals, i, 3, 9):
			pack9(residuals, i, fout)
			i += 9
		elif canPack(residuals, i, 4, 7):
			pack7(residuals, i, fout)
			i += 7
		elif canPack(residuals, i, 5, 5):
			pack5(residuals, i, fout)
			i += 5
		elif canPack(residuals, i, 7, 4):
			pack4(residuals, i, fout)
			i += 4
		elif canPack(residuals, i, 9, 3):
			pack3(residuals, i, fout)
			i += 3
		elif canPack(residuals, i, 14, 2):
			pack2(residuals, i, fout)
			i += 2
		elif canPack(residuals, i, 28, 1):
			pack1(residuals, i, fout)
			i += 1
		else:
			raise Exception('Unable to pack')
		l += 4
	return l

def decompress_generator(file_name, start, l):
	f = open(file_name, 'rb')

	f.seek(start)
	shift = 0

	data = []
	read_from_cur_data = 0

	while True and l > 0:

		if len(data) > read_from_cur_data:
			read_from_cur_data += 1
			yield data[read_from_cur_data - 1]
			continue

		# now we need to read more data from file
		data = []
		val = f.read(4)
		l -= 4

		if val == '':
			break

		val = ''.join(['{:08b}'.format(ord(c)) for c in val])
		val = int(val, 2)
		to = unpacks[val >> 28](val)
		to = to[::-1]

		for t in to:
			shift += t
			data.append(shift)

		read_from_cur_data = 1

		yield data[0]

	while len(data) > read_from_cur_data:
		read_from_cur_data += 1
		yield data[read_from_cur_data - 1]

	f.close()

def decompress(f, start, l):
	f.seek(start)

	data = set([])
	shift = 0

	while True and l > 0:
		val = f.read(4)
		# print('len', len(val))
		# for c in val:
		# 	print(ord(c))
		l -= 4

		if val == '':
			break

		val = ''.join(['{:08b}'.format(ord(c)) for c in val])
		# print(val)
		val = int(val, 2)
		to = unpacks[val >> 28](val)
		to = to[::-1]

		# print('val', val >> 28)
		# print('to', to)

		for t in to:
			shift += t
			data.add(shift)
	return data

def canPack(data, start, n_bits, n_values):
	# print(len(data) - start, n_values)
	if len(data) - start < n_values:
		return False

	n = min(len(data) - start, n_values)
	maxn = (1 << n_bits) - 1

	for i in range(start, start + n):
		# if n_bits == 1:
		#  	print('data[i]', data[i], maxn)
		if data[i] > maxn:
			return False
	# print('True', n_bits)
	return True

def pack28(data, start, fout):
	res = data[start] | data[start + 1]<<1 | data[start + 2]<<2 | data[start + 3]<<3 |\
			data[start + 4]<<4 | data[start + 5]<<5 | data[start + 6]<<6 | data[start + 7]<<7 | data[start + 8]<<8 | data[start + 9]<<9 | data[start + 10]<<10 | data[start + 11]<<11 |\
			data[start + 12]<<12 | data[start + 13]<<13 | data[start + 14]<<14 | data[start + 15]<<15 | data[start + 16]<<16 | data[start + 17]<<17 | data[start + 18]<<18 | data[start + 19]<<19 |\
			data[start + 20]<<20 | data[start + 21]<<21 | data[start + 22]<<22 | data[start + 23]<<23 | data[24]<<24 | data[start + 25]<<25 | data[start + 26]<<26 | data[start + 27]<<27

	res = '{:032b}'.format(res)

	for i in range(4):
		fout.write(chr(int(res[8 * i: 8 * i + 8], 2)))

def pack14(data, start, fout):
	res = 1<<28 | data[start] | data[start + 1]<<2 |\
			data[start + 2]<<4 | data[start + 3]<<6 | data[start + 4]<<8 | data[start + 5]<<10 |\
			data[start + 6]<<12 | data[start + 7]<<14 | data[start + 8]<<16 | data[start + 9]<<18 |\
			data[start + 10]<<20 | data[start + 11]<<22 | data[start + 12]<<24 | data[start + 13]<<26

	res = '{:032b}'.format(res)
	# print('PACKED data', data[start:start+14])
	# print('PACKED', res)

	for i in range(4):
		fout.write(chr(int(res[8 * i: 8 * i + 8], 2)))

def pack9(data, start, fout):
	res = 2<<28 | data[start] | data[start + 1]<<3 |\
			data[start + 2]<<6 | data[start + 3]<<9 | data[start + 4]<<12 | data[start + 5]<<15 |\
			data[start + 6]<<18 | data[start + 7]<<21 | data[start + 8]<<24

	res = '{:032b}'.format(res)

	for i in range(4):
		fout.write(chr(int(res[8 * i: 8 * i + 8], 2)))

def pack7(data, start, fout):
	res = 3<<28 | data[start] | data[start + 1]<<4 |\
			data[start + 2]<<8 | data[start + 3]<<12 | data[start + 4]<<16 | data[start + 5]<<20 |\
			data[start + 6]<<24

	res = '{:032b}'.format(res)

	for i in range(4):
		fout.write(chr(int(res[8 * i: 8 * i + 8], 2)))

def pack5(data, start, fout):
	res = 4<<28 | data[start] | data[start + 1]<<5 |\
			data[start + 2]<<10 | data[start + 3]<<15 | data[start + 4]<<20

	res = '{:032b}'.format(res)

	for i in range(4):
		fout.write(chr(int(res[8 * i: 8 * i + 8], 2)))

def pack4(data, start, fout):
	res = 5<<28 | data[start] | data[start + 1]<<7 |\
			data[start + 2]<<14 | data[start + 3]<<21

	res = '{:032b}'.format(res)

	for i in range(4):
		fout.write(chr(int(res[8 * i: 8 * i + 8], 2)))

def pack3(data, start, fout):
	res = 6<<28 | data[start] | data[start + 1]<<9 |\
			data[start + 2]<<18

	res = '{:032b}'.format(res)

	for i in range(4):
		fout.write(chr(int(res[8 * i: 8 * i + 8], 2)))

def pack2(data, start, fout):
	res = 7<<28 | data[start] | data[start + 1]<<14

	res = '{:032b}'.format(res)

	for i in range(4):
		fout.write(chr(int(res[8 * i: 8 * i + 8], 2)))

def pack1(data, start, fout):
	res = 8<<28 | data[start]

	res = '{:032b}'.format(res)

	for i in range(4):
		fout.write(chr(int(res[8 * i: 8 * i + 8], 2)))

def unpack28(val):
	st = []
	st.append((val >> 27) & 1)
	st.append((val >> 26) & 1)
	st.append((val >> 25) & 1)
	st.append((val >> 24) & 1)
	st.append((val >> 23) & 1)
	st.append((val >> 22) & 1)
	st.append((val >> 21) & 1)
	st.append((val >> 20) & 1)
	st.append((val >> 19) & 1)
	st.append((val >> 18) & 1)
	st.append((val >> 17) & 1)
	st.append((val >> 16) & 1)
	st.append((val >> 15) & 1)
	st.append((val >> 14) & 1)
	st.append((val >> 13) & 1)
	st.append((val >> 12) & 1)
	st.append((val >> 11) & 1)
	st.append((val >> 10) & 1)
	st.append((val >> 9) & 1)
	st.append((val >> 8) & 1)
	st.append((val >> 7) & 1)
	st.append((val >> 6) & 1)
	st.append((val >> 5) & 1)
	st.append((val >> 4) & 1)
	st.append((val >> 3) & 1)
	st.append((val >> 2) & 1)
	st.append((val >> 1) & 1)
	st.append(val & 1)
	return st
def unpack14(val):
	st = []
	st.append((val >> 26) & 3)
	st.append((val >> 24) & 3)
	st.append((val >> 22) & 3)
	st.append((val >> 20) & 3)
	st.append((val >> 18) & 3)
	st.append((val >> 16) & 3)
	st.append((val >> 14) & 3)
	st.append((val >> 12) & 3)
	st.append((val >> 10) & 3)
	st.append((val >> 8) & 3)
	st.append((val >> 6) & 3)
	st.append((val >> 4) & 3)
	st.append((val >> 2) & 3)
	st.append(val & 3)
	return st
def unpack9(val):
	st = []
	st.append((val >> 24) & 7)
	st.append((val >> 21) & 7)
	st.append((val >> 18) & 7)
	st.append((val >> 15) & 7)
	st.append((val >> 12) & 7)
	st.append((val >> 9) & 7)
	st.append((val >> 6) & 7)
	st.append((val >> 3) & 7)
	st.append(val & 7)
	return st
def unpack7(val):
	st = []
	st.append((val >> 24) & 15)
	st.append((val >> 20) & 15)
	st.append((val >> 16) & 15)
	st.append((val >> 12) & 15)
	st.append((val >> 8) & 15)
	st.append((val >> 4) & 15)
	st.append( val & 15)
	return st
	0100100
def unpack5(val):
	st = []
	st.append((val >> 20) & 31)
	st.append((val >> 15) & 31)
	st.append((val >> 10) & 31)
	st.append((val >> 5) & 31)
	st.append((val >> 0) & 31)
	return st
def unpack4(val):
	st = []
	st.append((val >> 21) & 127)
	st.append((val >> 14) & 127)
	st.append((val >> 7) & 127)
	st.append(val & 127)
	return st
def unpack3(val):
	st = []
	st.append((val >> 18) & 511)
	st.append((val >> 9) & 511)
	st.append(val & 511)
	return st
def unpack2(val):
	st = []
	st.append((val >> 14) & 16383)
	st.append(val & 16383)
	return st
def unpack1(val):
	st = []
	st.append(val & 268435455)
	return st

unpacks = [unpack28, unpack14, unpack9, unpack7, unpack5, unpack4, unpack3, unpack2, unpack1]


# arr = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 213, 214, 215, 216, 217, 218, 219, 221, 222, 223, 224, 225, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 279, 281, 282, 284, 285, 286, 287, 288, 289, 291, 292, 293, 294, 295, 296, 297, 298, 300, 301, 302, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 315, 316, 317, 318, 320, 322, 323, 324, 325, 326, 327, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 371, 372, 373, 377, 378, 379, 380, 381, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 416, 417, 418, 419, 420, 422, 423, 424, 425, 427, 428, 429, 430, 431, 432, 433, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 453, 454, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 481, 482, 483, 487, 489, 490, 491, 492, 493, 494, 495, 496, 497, 499, 500, 501, 502, 503, 504, 505, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 525, 526, 527, 529, 530, 531, 532, 533, 534, 535, 536, 538, 539, 540, 541, 542, 543, 544, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 687, 688, 690, 691, 692, 693, 694, 695, 696, 697, 699, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 732, 733, 735, 736, 737, 738, 739, 742, 744, 745, 746, 747, 748, 749, 750, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 787, 788, 789, 790, 791, 792, 793, 794, 795, 797, 798, 799, 800, 801, 802, 804, 805, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 826, 828, 829, 830, 831, 832, 834, 835, 836, 837, 838, 840, 841, 842, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 855, 856, 857, 860, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 876, 877, 878, 879, 880, 881, 882, 883, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 929, 930, 931, 932, 933, 934, 935, 936, 938, 939, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 954, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1052, 1053, 1054, 1056, 1057, 1058, 1059, 1060, 1061, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1099, 1100, 1101, 1104, 1105, 1106, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1116, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1128, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1193, 1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1218, 1219, 1220, 1221, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1245, 1246, 1247, 1248, 1250, 1251, 1252, 1253, 1254, 1256, 1257, 1258, 1259, 1261, 1262, 1264, 1265, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1274]
# arr = arr[:28]

# with open('../bin.out', 'wb') as f:
# 	# l1 = compress([1, 2, 3], f)
#  	l2 = compress(arr,f)
#  	# l3 = compress([100, 200, 300], f)
# with open('../bin.out', 'rb') as f:
#  	st = sorted(decompress(f, 0, l2))
# print('\n\n')
# print(arr)
# print('\n\n')
# print(sorted(st))

# for i in range(len(arr)):
# 	if arr[i] != st[i]:
# 		print(i)
# 		break