water.sf = csv_reader('water_00.csv');
water.md = csv_reader('water_06.csv');
water.bt = csv_reader('water_11.csv');

save('water.mat','water','-v7.3','-nocompression');