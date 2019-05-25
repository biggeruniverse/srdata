#(c) 2012 savagerebirth.com

class TitheSettings(DefaultContainer):

	def __init__(self):
		DefaultContainer.__init__(self);
			
		self.setSize(178, 136);
		#self.setPosition(370, screenHeight - 210);
		#self.setBackgroundColor( glass.Color(0,0,0,128));
		#self.setVisible(0);

		self.table = DefaultTable();
		self.table.setFrame(0);
		self.add(self.table,10,10);
		taxRateLabel = DefaultLabel("Tax Rate%:");
		taxRateLabel.setFont(fontSizeSmall);
		taxRate = DefaultSpinner();
		taxRate.linkCvar("sv_tithe_display");
		taxRate.setMinMax(1,100);
		taxRate.addValueListener(self);
		self.table.addRow(taxRateLabel, taxRate);

		reserveLabel = DefaultLabel("Reserve:");
		reserveLabel.setFont(fontSizeSmall);
		reserve = DefaultSpinner();
		reserve.setStep(100);
		reserve.setMinMax(0,50000);
		reserve.linkCvar("cl_cmdr_goldReserve");
		self.table.addRow(reserveLabel, reserve);

		enforceLabel = DefaultLabel("Enforce Reserve: ");
		enforceLabel.setFont(fontSizeSmall);
		enforce = DefaultCheckBox();
		enforce.linkCvar("cl_cmdr_enforceReserve");
		self.table.addRow(enforceLabel, enforce);

	def toggle(self):
		if self.isVisible():
			self.setVisible(0);
		else:
			self.setVisible(1);

	def onValueChanged(self, e):
		CL_UpdateTithe(int(cvar_getvalue("sv_tithe_display")));	