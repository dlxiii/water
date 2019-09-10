water_surface = csv_reader('water_surface.csv');
water_middle = csv_reader('water_middle.csv');
water_bottom = csv_reader('water_bottom.csv');

save('water_surface.mat','water_surface','-v7.3','-nocompression');
save('water_middle.mat','water_middle','-v7.3','-nocompression');
save('water_bottom.mat','water_bottom','-v7.3','-nocompression');