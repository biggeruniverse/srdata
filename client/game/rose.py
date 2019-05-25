

CL_MinimapClear();
CL_MinimapStartDraw(3200, 3200, 0.0, 1.0);

for theta in range(0,360,5):
	rho = math.radians(theta)
	r = math.sin ((4.0/1.0) * rho);
	x = r * math.cos(rho);
	y = r * math.sin(rho);

	CL_MinimapAddPoint(x*3200+3200, y*3200+3200, 0.0, 1.0);

CL_MinimapAddPoint(3200, 3200, 0.0, 1.0);
CL_MinimapEndDraw();
