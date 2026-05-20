from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView

class Ticket3D:
    def __init__(self, num):
        self.num = num
        self.bai = num // 100
        self.shi = (num // 10) % 10
        self.wei = num % 10
    
    @property
    def digits(self):
        return (self.bai, self.shi, self.wei)
    
    def sum(self):
        return sum(self.digits)
    
    def span(self):
        return max(self.digits) - min(self.digits)

ALL_TICKETS = [Ticket3D(i) for i in range(1000)]

class DanmaPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        
        self.add_widget(Label(text='财富广场彩票站', font_size=16, color=(1, 0, 0, 1)))
        self.add_widget(Label(text='微信手机: 132 9699 9092', font_size=14, color=(1, 0, 0, 1)))
        self.add_widget(Label(text='定胆号码', font_size=18, bold=True))
        
        grid = GridLayout(cols=10, spacing=5)
        self.checkboxes = []
        for i in range(10):
            cb = CheckBox(active=True, size_hint=(None, None), size=(40, 40))
            self.checkboxes.append(cb)
            grid.add_widget(cb)
            grid.add_widget(Label(text=str(i), font_size=14))
        self.add_widget(grid)
        
        btn_layout = BoxLayout(spacing=10)
        self.select_all_btn = Button(text='全选', on_press=self.select_all)
        self.clear_btn = Button(text='清空', on_press=self.clear_all)
        btn_layout.add_widget(self.select_all_btn)
        btn_layout.add_widget(self.clear_btn)
        self.add_widget(btn_layout)
    
    def select_all(self, instance):
        for cb in self.checkboxes:
            cb.active = True
    
    def clear_all(self, instance):
        for cb in self.checkboxes:
            cb.active = False
    
    def get_values(self):
        return [i for i, cb in enumerate(self.checkboxes) if cb.active]

class SumSpanPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        
        self.add_widget(Label(text='和值/跨度', font_size=18, bold=True))
        
        self.add_widget(Label(text='和尾:'))
        tail_grid = GridLayout(cols=10, spacing=5)
        self.tail_checkboxes = []
        for i in range(10):
            cb = CheckBox(active=True, size_hint=(None, None), size=(30, 30))
            self.tail_checkboxes.append(cb)
            tail_grid.add_widget(cb)
            tail_grid.add_widget(Label(text=str(i), font_size=12))
        self.add_widget(tail_grid)
        
        self.add_widget(Label(text='跨度:'))
        span_grid = GridLayout(cols=10, spacing=5)
        self.span_checkboxes = []
        for i in range(10):
            cb = CheckBox(active=True, size_hint=(None, None), size=(30, 30))
            self.span_checkboxes.append(cb)
            span_grid.add_widget(cb)
            span_grid.add_widget(Label(text=str(i), font_size=12))
        self.add_widget(span_grid)
    
    def get_values(self):
        tails = [i for i, cb in enumerate(self.tail_checkboxes) if cb.active]
        spans = [i for i, cb in enumerate(self.span_checkboxes) if cb.active]
        return {'tails': tails, 'spans': spans}

class PositionPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        
        self.add_widget(Label(text='定位胆码', font_size=18, bold=True))
        
        self.add_widget(Label(text='百位:'))
        bai_grid = GridLayout(cols=10, spacing=5)
        self.bai_checkboxes = []
        for i in range(10):
            cb = CheckBox(active=True, size_hint=(None, None), size=(30, 30))
            self.bai_checkboxes.append(cb)
            bai_grid.add_widget(cb)
            bai_grid.add_widget(Label(text=str(i), font_size=12))
        self.add_widget(bai_grid)
        
        self.add_widget(Label(text='十位:'))
        shi_grid = GridLayout(cols=10, spacing=5)
        self.shi_checkboxes = []
        for i in range(10):
            cb = CheckBox(active=True, size_hint=(None, None), size=(30, 30))
            self.shi_checkboxes.append(cb)
            shi_grid.add_widget(cb)
            shi_grid.add_widget(Label(text=str(i), font_size=12))
        self.add_widget(shi_grid)
        
        self.add_widget(Label(text='个位:'))
        wei_grid = GridLayout(cols=10, spacing=5)
        self.wei_checkboxes = []
        for i in range(10):
            cb = CheckBox(active=True, size_hint=(None, None), size=(30, 30))
            self.wei_checkboxes.append(cb)
            wei_grid.add_widget(cb)
            wei_grid.add_widget(Label(text=str(i), font_size=12))
        self.add_widget(wei_grid)
    
    def get_values(self):
        bai = [i for i, cb in enumerate(self.bai_checkboxes) if cb.active]
        shi = [i for i, cb in enumerate(self.shi_checkboxes) if cb.active]
        wei = [i for i, cb in enumerate(self.wei_checkboxes) if cb.active]
        return {'bai': bai, 'shi': shi, 'wei': wei}

class ResultPanel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results_label = Label(text='', font_size=14, size_hint_y=None, text_size=(self.width, None))
        self.results_label.bind(width=self.update_text_size)
        self.add_widget(self.results_label)
    
    def update_text_size(self, instance, width):
        self.results_label.text_size = (width - 20, None)
    
    def set_results(self, tickets):
        if not tickets:
            self.results_label.text = '没有符合条件的号码'
        else:
            lines = [f"{t.num:03d}" for t in tickets]
            formatted = []
            for i in range(0, len(lines), 5):
                formatted.append(' '.join(lines[i:i+5]))
            self.results_label.text = '\n'.join(formatted)
        self.results_label.height = max(self.results_label.texture_size[1], 100)

class FilterApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        self.main_scroll = ScrollView()
        self.main_content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.main_content.bind(minimum_height=self.main_content.setter('height'))
        
        self.danma_panel = DanmaPanel()
        self.main_content.add_widget(self.danma_panel)
        
        self.sum_span_panel = SumSpanPanel()
        self.main_content.add_widget(self.sum_span_panel)
        
        self.position_panel = PositionPanel()
        self.main_content.add_widget(self.position_panel)
        
        self.filter_btn = Button(text='开始缩水', on_press=self.run_filter, size_hint=(1, None), height=60, font_size=20)
        self.main_content.add_widget(self.filter_btn)
        
        self.reset_btn = Button(text='重置条件', on_press=self.reset_conditions, size_hint=(1, None), height=50)
        self.main_content.add_widget(self.reset_btn)
        
        self.count_label = Label(text='剩余注数: 1000', font_size=16, size_hint=(1, None), height=40)
        self.main_content.add_widget(self.count_label)
        
        self.main_scroll.add_widget(self.main_content)
        self.root.add_widget(self.main_scroll)
        
        self.result_panel = ResultPanel(size_hint=(1, 0.4))
        self.root.add_widget(self.result_panel)
        
        return self.root
    
    def run_filter(self, instance):
        danma = self.danma_panel.get_values()
        sum_span = self.sum_span_panel.get_values()
        position = self.position_panel.get_values()
        
        results = []
        for ticket in ALL_TICKETS:
            if danma and not any(d in danma for d in ticket.digits):
                continue
            
            if sum_span['tails'] and ticket.sum() % 10 not in sum_span['tails']:
                continue
            
            if sum_span['spans'] and ticket.span() not in sum_span['spans']:
                continue
            
            if position['bai'] and ticket.bai not in position['bai']:
                continue
            if position['shi'] and ticket.shi not in position['shi']:
                continue
            if position['wei'] and ticket.wei not in position['wei']:
                continue
            
            results.append(ticket)
        
        self.count_label.text = f'剩余注数: {len(results)}'
        self.result_panel.set_results(results)
    
    def reset_conditions(self, instance):
        self.danma_panel.select_all(None)
        
        for cb in self.sum_span_panel.tail_checkboxes:
            cb.active = True
        for cb in self.sum_span_panel.span_checkboxes:
            cb.active = True
        
        for cb in self.position_panel.bai_checkboxes:
            cb.active = True
        for cb in self.position_panel.shi_checkboxes:
            cb.active = True
        for cb in self.position_panel.wei_checkboxes:
            cb.active = True
        
        self.count_label.text = '剩余注数: 1000'
        self.result_panel.set_results(ALL_TICKETS)

if __name__ == '__main__':
    FilterApp().run()
