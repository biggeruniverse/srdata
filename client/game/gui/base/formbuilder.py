# (c) 2011 savagerebirth.com

import glass;

# TODO: the table should be created and passed to construct(). Done this way because of rushness, should be revisited later

def construct(build, width=200, height=300):
    
    builder = formbuilder.Builder();
    
    table = DefaultTable();
    table.setFrame(0);
    table.horizontalJustification = glass.Graphics.LEFT;
    table.setSize(width, height);
    table.setCellPadding(5);
    
    con_println("\nBuilding form...\n");
    
    # I want the first row to be darker so adding an empty row... this is bad practice :)
    #firstRow = table.addRow("", DefaultLabel(""));
    
    for name, data in build.items():
        con_println("\t* adding " + str(data['widget']) + "\n");        
        method = getattr(builder, 'create' + data['widget'], builder.createWidget);
        table.addRow(name, method(data));
    
    con_println("------------\n");
        
    # TODO: this shouldnt be hardcoded in the builder
    table.adjustSizeTo(width - 60); # has to take into account padding and the scrollbar
    
    #firstRow.setHeight(0);
        
    return table;
        
class Builder():
    
    x = 0;
    padding = 10;
    
    def addRow(self, name, widget, data, description=""):
        pass;
        # create container for the row
        # set full widget of main container
        
        # set inner container for row padding
        
        # create container for left column and cell padding
        
        # add name to it
        
        # create container for right column and cell padding
        
        # add the widget
        
        # add the description if there is one
        
        
    def createDropDown(self, data):
        
        if data.has_key("caption"):
            data["_caption"] = data["caption"];
            data.remove_key("caption");
        
        obj = self.createWidget(data);
        
        if data.has_key("_caption"):
            obj.setCaption(data["_caption"]);
        
        for name, value in data['options'].items():
            obj.addOption(name, value);
            
        if data.has_key("selectionListener"):
            obj.addSelectionListener(data["selectionListener"]);
            
        return obj;
            
    def createSlider(self, data):
        obj = self.createWidget(data);
        
        if data.has_key("scaleEnd"):
            obj.setScaleEnd(data["scaleEnd"]);
        
        if data.has_key("scaleStart"):
            obj.setScaleStart(data["scaleStart"]);
        
        return obj;    
            
    def createSpinner(self, data):
        obj = self.createWidget(data);
        
        if data.has_key("step"):
            obj.setStep(data["step"]);
            
        return obj;

    def createWidget(self, data):
        
        import __main__;
        widget = getattr(__main__, "Default" + data["widget"]);
        
        if data.has_key("caption"):
            obj = widget(data["caption"]);
        else:
            obj = widget();
        
        if data.has_key("cvar"):
            obj.linkCvar(data["cvar"]);
            
        if data.has_key("clickAction"):
            obj.setClickAction(data["clickAction"]);
            
        return obj;
