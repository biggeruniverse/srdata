# (c) 2012 savagerebirth.com

#FIXME: Needs some paging mechanism
class CommSelection(CommAbstractWidget):
    
	def create(self):
		self.setPosition(screenWidth - 132, screenHeight - 132);
		self.setBackgroundColor( glass.Color(0,0,0,128));
		self.setSize(132, 122);

		self.selLabels = [];

	def rebuild(self):
		pass;

	def frame(self):
		for l in self.selLabels:
			l.setVisible(0);
		for i,obj in enumerate(commhud.selection.list):
			if commhud.team.teamId != obj.getTeam():
				continue;
			if i >= len(self.selLabels):
				l = DefaultLabel();
				self.selLabels.append(l);
				self.add(l);
			else:
				l = self.selLabels[i];
			l.setImage(obj.getIcon());
			l.setSize(24,24);

			k = obj.getHealthPct();
			hue = (k-0.1)/2.7 if k > 0.1 else 0;

			l.setForegroundColor(tools.HSLColor(hue,1.0,0.5));
			l.setVisible(1);

		x=0;
		y=0;
		for l in self.selLabels:
			if l.isVisible():
				l.setPosition(x, y);
				x+=24;
			if x>=120:
				x=0;
				y+=24;

#comsel = CommSelection();
#commhud.addWidget('selection', comsel);
