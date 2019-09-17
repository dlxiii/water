water.sf = csv_reader('water_surface.csv');
water.md = csv_reader('water_middle.csv');
water.bt = csv_reader('water_bottom.csv');

save('water.mat','water','-v7.3','-nocompression');