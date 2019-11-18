import wx
import wx.xrc
import wx.richtext as rt
from cvProcessor import CVProcessor
from clipsUtil import CLIPS


class GUI(wx.Frame):
    def __init__(self, parent, config):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="PAITEN EX KELIPS",
            pos=wx.DefaultPosition,
            size=wx.Size(1280, 768),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL
        )

        self.config = config
        self.clips = None

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(208, 208, 208))

        outer_layout = wx.FlexGridSizer(2, 1, 0, 0)
        outer_layout.AddGrowableCol(0)
        outer_layout.AddGrowableRow(0)
        outer_layout.AddGrowableRow(1)
        outer_layout.SetFlexibleDirection(wx.BOTH)
        outer_layout.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        inner_layout_top = wx.FlexGridSizer(0, 3, 0, 0)
        inner_layout_top.AddGrowableCol(0)
        inner_layout_top.AddGrowableCol(1)
        inner_layout_top.AddGrowableCol(2)
        inner_layout_top.AddGrowableRow(0)
        inner_layout_top.SetFlexibleDirection(wx.BOTH)
        inner_layout_top.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.source_image_panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.source_image_panel.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_APPWORKSPACE)
        )

        self.source_panel_layout = wx.BoxSizer(wx.VERTICAL)

        self.source_panel_title = wx.StaticText(
            self.source_image_panel, wx.ID_ANY, u"Source Image", wx.DefaultPosition, wx.DefaultSize,
            0
        )
        self.source_panel_title.Wrap(-1)

        self.source_panel_layout.Add(
            self.source_panel_title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5
        )

        self.source_panel_image = wx.StaticBitmap(
            self.source_image_panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition,
            wx.Size(300, 300), 0
        )
        self.source_panel_layout.Add(self.source_panel_image, 1, wx.EXPAND | wx.ALL, 5)

        self.source_image_panel.SetSizer(self.source_panel_layout)
        self.source_image_panel.Layout()
        self.source_panel_layout.Fit(self.source_image_panel)
        inner_layout_top.Add(self.source_image_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.detection_image_panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.detection_image_panel.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_APPWORKSPACE)
        )

        detection_image_layout = wx.BoxSizer(wx.VERTICAL)

        self.detection_image_title = wx.StaticText(
            self.detection_image_panel, wx.ID_ANY, u"Detection Image", wx.DefaultPosition,
            wx.DefaultSize, 0
        )
        self.detection_image_title.Wrap(-1)

        detection_image_layout.Add(
            self.detection_image_title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5
        )

        self.detection_image_title = wx.StaticBitmap(
            self.detection_image_panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition,
            wx.Size(300, 300), 0
        )
        detection_image_layout.Add(self.detection_image_title, 1, wx.ALL | wx.EXPAND, 5)

        self.detection_image_panel.SetSizer(detection_image_layout)
        self.detection_image_panel.Layout()
        detection_image_layout.Fit(self.detection_image_panel)
        inner_layout_top.Add(self.detection_image_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.control_panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.control_panel.SetBackgroundColour(wx.Colour(208, 208, 208))

        control_layout = wx.BoxSizer(wx.VERTICAL)

        self.open_image_button = wx.Button(
            self.control_panel, wx.ID_ANY, u"Open Image", wx.DefaultPosition, wx.DefaultSize, 0
        )
        control_layout.Add(
            self.open_image_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5
        )

        self.open_rule_button = wx.Button(
            self.control_panel, wx.ID_ANY, u"Open Rule Editor", wx.DefaultPosition, wx.DefaultSize,
            0
        )
        control_layout.Add(
            self.open_rule_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5
        )

        self.show_rules_button = wx.Button(
            self.control_panel, wx.ID_ANY, u"Show Rules", wx.DefaultPosition, wx.DefaultSize, 0
        )
        control_layout.Add(
            self.show_rules_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5
        )

        self.show_facts_button = wx.Button(
            self.control_panel, wx.ID_ANY, u"Show Facts", wx.DefaultPosition, wx.DefaultSize, 0
        )
        control_layout.Add(
            self.show_facts_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5
        )

        self.control_text = wx.StaticText(
            self.control_panel, wx.ID_ANY, u"What shape do you want?", wx.DefaultPosition,
            wx.DefaultSize, 0
        )
        self.control_text.Wrap(-1)

        control_layout.Add(self.control_text, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 10)

        self.shape_selector = wx.TreeCtrl(
            self.control_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE
        )

        all_shapes = self.shape_selector.AddRoot('Semua Bentuk')

        irregular_triangle = self.shape_selector.AppendItem(all_shapes, "Segitiga Tidak Beraturan")
        irregular_square = self.shape_selector.AppendItem(all_shapes, "Segiempat Tidak Beraturan")
        irregular_pentagon = self.shape_selector.AppendItem(all_shapes, "Segilima Tidak Beraturan")
        irregular_hexagon = self.shape_selector.AppendItem(all_shapes, "Segienam Tidak Beraturan")

        acute_triangle = self.shape_selector.AppendItem(irregular_triangle, "Segitiga Lancip")
        obtuse_triangle = self.shape_selector.AppendItem(irregular_triangle, "Segitiga Tumpul")
        right_triangle = self.shape_selector.AppendItem(irregular_triangle, "Segitiga Siku-Siku")
        isosceles_triangle = self.shape_selector.AppendItem(
            irregular_triangle, "Segitiga Sama Kaki"
        )
        equilateral_triangle = self.shape_selector.AppendItem(
            irregular_triangle, "Segitiga Sama Sisi"
        )
        parallelogram = self.shape_selector.AppendItem(irregular_square, "Jajaran Genjang")
        trapezoid = self.shape_selector.AppendItem(irregular_square, "Trapesium")
        equilateral_pentagon = self.shape_selector.AppendItem(
            irregular_pentagon, "Segilima Sama Sisi"
        )
        equilateral_hexagon = self.shape_selector.AppendItem(
            irregular_hexagon, "Segienam Sama Sisi"
        )

        isosceles_right_triangle = self.shape_selector.AppendItem(
            isosceles_triangle, "Segitiga Sama Kaki dan Siku-Siku"
        )
        isosceles_obtuse_triangle = self.shape_selector.AppendItem(
            isosceles_triangle, "Segitiga Sama Kaki dan Tumpul"
        )
        isosceles_acute_triangle = self.shape_selector.AppendItem(
            isosceles_triangle, "Segitiga Sama Kaki dan Lancip"
        )
        isosceles_acute_triangle = self.shape_selector.AppendItem(
            isosceles_triangle, "Segitiga Sama Kaki dan Lancip"
        )
        regular_square = self.shape_selector.AppendItem(parallelogram, "Segiempat Beraturan")
        kite_shaped_square = self.shape_selector.AppendItem(
            parallelogram, "Segiempat bentuk Layang-Layang"
        )
        isosceles_trapezoid = self.shape_selector.AppendItem(trapezoid, "Trapesium Sama Kaki")
        right_aligned_trapezoid = self.shape_selector.AppendItem(trapezoid, "Trapesium Rata Kanan")
        left_aligned_trapezoid = self.shape_selector.AppendItem(trapezoid, "Trapesium Rata Kiri")

        control_layout.Add(
            self.shape_selector, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.RIGHT | wx.LEFT, 10
        )

        self.control_panel.SetSizer(control_layout)
        self.control_panel.Layout()
        control_layout.Fit(self.control_panel)
        inner_layout_top.Add(self.control_panel, 1, wx.EXPAND | wx.ALL, 5)

        outer_layout.Add(inner_layout_top, 1, wx.EXPAND, 5)

        inner_layout_bottom = wx.FlexGridSizer(0, 3, 0, 0)
        inner_layout_bottom.AddGrowableCol(0)
        inner_layout_bottom.AddGrowableCol(1)
        inner_layout_bottom.AddGrowableCol(2)
        inner_layout_bottom.AddGrowableRow(0)
        inner_layout_bottom.SetFlexibleDirection(wx.BOTH)
        inner_layout_bottom.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.detection_result_panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.detection_result_panel.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_APPWORKSPACE)
        )

        detection_result_layout = wx.BoxSizer(wx.VERTICAL)

        self.detection_result_title = wx.StaticText(
            self.detection_result_panel, wx.ID_ANY, u"Detection Result", wx.DefaultPosition,
            wx.DefaultSize, 0
        )
        self.detection_result_title.Wrap(-1)

        detection_result_layout.Add(
            self.detection_result_title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5
        )

        detection_result_listChoices = []
        self.detection_result_list = wx.ListBox(
            self.detection_result_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            detection_result_listChoices, 0
        )
        detection_result_layout.Add(self.detection_result_list, 1, wx.ALL | wx.EXPAND, 5)

        self.detection_result_panel.SetSizer(detection_result_layout)
        self.detection_result_panel.Layout()
        detection_result_layout.Fit(self.detection_result_panel)
        inner_layout_bottom.Add(self.detection_result_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.matched_facts_panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.matched_facts_panel.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_APPWORKSPACE)
        )

        matched_facts_layout = wx.BoxSizer(wx.VERTICAL)

        self.mathced_facts_title = wx.StaticText(
            self.matched_facts_panel, wx.ID_ANY, u"Matched Facts", wx.DefaultPosition,
            wx.DefaultSize, 0
        )
        self.mathced_facts_title.Wrap(-1)

        matched_facts_layout.Add(
            self.mathced_facts_title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5
        )

        matched_facts_listChoices = []
        self.matched_facts_list = wx.ListBox(
            self.matched_facts_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            matched_facts_listChoices, 0
        )
        matched_facts_layout.Add(self.matched_facts_list, 1, wx.ALL | wx.EXPAND, 5)

        self.matched_facts_panel.SetSizer(matched_facts_layout)
        self.matched_facts_panel.Layout()
        matched_facts_layout.Fit(self.matched_facts_panel)
        inner_layout_bottom.Add(self.matched_facts_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.hit_rules_panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.hit_rules_panel.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_APPWORKSPACE)
        )

        hit_rules_layout = wx.BoxSizer(wx.VERTICAL)

        self.hit_rules_title = wx.StaticText(
            self.hit_rules_panel, wx.ID_ANY, u"Hit Rules", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.hit_rules_title.Wrap(-1)

        hit_rules_layout.Add(self.hit_rules_title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        hit_rules_listChoices = []
        self.hit_rules_list = wx.ListBox(
            self.hit_rules_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            hit_rules_listChoices, 0
        )
        hit_rules_layout.Add(self.hit_rules_list, 1, wx.ALL | wx.EXPAND, 5)

        self.hit_rules_panel.SetSizer(hit_rules_layout)
        self.hit_rules_panel.Layout()
        hit_rules_layout.Fit(self.hit_rules_panel)
        inner_layout_bottom.Add(self.hit_rules_panel, 1, wx.EXPAND | wx.ALL, 5)

        outer_layout.Add(inner_layout_bottom, 1, wx.EXPAND, 5)

        self.SetSizer(outer_layout)
        self.Layout()

        self.Centre(wx.BOTH)

        self.open_image_button.Bind(wx.EVT_BUTTON, self.onOpenImageClicked)
        self.shape_selector.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onShapeSelect)
        self.open_rule_button.Bind(wx.EVT_BUTTON, self.onOpenEditor)
        self.show_facts_button.Bind(wx.EVT_BUTTON, self.onShowFacts)
        self.show_rules_button.Bind(wx.EVT_BUTTON, self.onShowRules)

    def onOpenImageClicked(self, event):
        btn = event.GetEventObject().GetLabel()
        print("Label of pressed button = ", btn)
        with wx.FileDialog(
            self,
            "Open Image",
            wildcard="Image files (*.jpg;*.png;*.jpeg)|*.jpg;*.png;*.jpeg",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            print(pathname)
            image = wx.Image(pathname, wx.BITMAP_TYPE_ANY)
            width, height = self.source_panel_image.GetClientSize()
            image = image.Scale(width, height)

            self.source_panel_image.SetBitmap(wx.Bitmap(image))
            self.source_panel_layout.RecalcSizes()

            shape_list = CVProcessor.processImage(pathname, self.config)
            self.clips = CLIPS(self.config, shape_list)
            self.clips.getRules()

    def onShapeSelect(self, event):
        print(self.shape_selector.GetItemText(event.GetItem()))

    def onOpenEditor(self, event):
        try:
            with open(self.config['kbs_file'], 'r') as file:
                data = file.read()
        except:
            raise Exception('File not found')
        editor = Editor(None, self.config, data)
        editor.Show()

    def onShowRules(self, event):
        try:
            with open(self.config['kbs_file'], 'r') as file:
                data = file.read()
        except:
            raise Exception('File not found')
        rules = ReadOnlyWindow(None, "All Rules", data)
        rules.Show()

    def onShowFacts(self, event):
        try:
            with open(self.config['kbs_file'], 'r') as file:
                data = file.read()
        except:
            raise Exception('File not found')
        rules = ReadOnlyWindow(None, "All Rules", data)
        rules.Show()

    def __del__(self):
        pass


class Editor(wx.Frame):
    def __init__(self, parent, config, text_data=''):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            pos=wx.DefaultPosition,
            size=wx.Size(600, 600),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL
        )

        self.config = config
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_layout = wx.BoxSizer(wx.VERTICAL)

        toolbar_layout = wx.BoxSizer(wx.HORIZONTAL)

        self.save_button = wx.Button(
            self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0
        )
        toolbar_layout.Add(self.save_button, 0, wx.ALL, 5)

        self.exit_button = wx.Button(
            self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0
        )
        toolbar_layout.Add(self.exit_button, 0, wx.ALL, 5)

        main_layout.Add(toolbar_layout, 0, 0, 5)

        self.rich_text = rt.RichTextCtrl(
            self, wx.ID_ANY, text_data, wx.DefaultPosition, wx.DefaultSize, 0
        )
        main_layout.Add(self.rich_text, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(main_layout)
        self.Layout()

        self.Centre(wx.BOTH)
        self.save_button.Bind(wx.EVT_BUTTON, self.onSave)
        self.exit_button.Bind(wx.EVT_BUTTON, self.onExit)

    def onSave(self, event):
        try:
            with open(self.config['kbs_file'], "w") as output:
                output.write(self.rich_text.GetValue())
        except Exception as e:
            raise Exception('Fail to save')
            print(e)

    def onExit(self, event):
        self.Close()

    def __del__(self):
        pass


class ReadOnlyWindow(wx.Frame):
    def __init__(self, parent, title, text_data):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=title,
            pos=wx.DefaultPosition,
            size=wx.Size(500, 500),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL
        )
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_layout = wx.BoxSizer(wx.VERTICAL)

        self.text = rt.RichTextCtrl(
            self, wx.ID_ANY, text_data, wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.text.Enable(False)

        main_layout.Add(self.text, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(main_layout)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


if __name__ == '__main__':
    app = wx.App()
    frm = GUI(None)

    # Show it.
    frm.Show()

    # Start the event loop.
    app.MainLoop()
