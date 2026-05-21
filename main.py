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

class FilterApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        root.add_widget(Label(text='3D彩票缩水', font_size=28, bold=True))
        
        info_layout = BoxLayout(orientation='vertical', spacing=5)
        info_layout.add_widget(Label(text='财富广场彩票站', font_size=16, color=(1, 0, 0, 1)))
        info_layout.add_widget(Label(text='微信: 13296999092', font_size=14, color=(1, 0, 0, 1)))
        root.add_widget(info_layout)
        
        root.add_widget(Label(text='--- 定胆号码 ---', font_size=16))
        danma_grid = GridLayout(cols=5, spacing=10)
        self.danma_cbs = []
        for i in range(10):
            cb = CheckBox(active=True)
            self.danma_cbs.append(cb)
            danma_grid.add_widget(cb)
            danma_grid.add_widget(Label(text=str(i), font_size=16))
        root.add_widget(danma_grid)
        
        danma_btns = BoxLayout(spacing=15)
        danma_btns.add_widget(Button(text='全选', on_press=self.select_all_danma, size_hint=(0.5, 1)))
        danma_btns.add_widget(Button(text='清空', on_press=self.clear_all_danma, size_hint=(0.5, 1)))
        root.add_widget(danma_btns)
        
        root.add_widget(Label(text='--- 和尾 ---', font_size=16))
        tail_grid = GridLayout(cols=5, spacing=10)
        self.tail_cbs = []
        for i in range(10):
            cb = CheckBox(active=True)
            self.tail_cbs.append(cb)
            tail_grid.add_widget(cb)
            tail_grid.add_widget(Label(text=str(i), font_size=14))
        root.add_widget(tail_grid)
        
        root.add_widget(Label(text='--- 跨度 ---', font_size=16))
        span_grid = GridLayout(cols=5, spacing=10)
        self.span_cbs = []
        for i in range(10):
            cb = CheckBox(active=True)
            self.span_cbs.append(cb)
            span_grid.add_widget(cb)
            span_grid.add_widget(Label(text=str(i), font_size=14))
        root.add_widget(span_grid)
        
        root.add_widget(Label(text='--- 定位胆码 ---', font_size=16))
        
        root.add_widget(Label(text='百位', font_size=14))
        bai_grid = GridLayout(cols=5, spacing=10)
        self.bai_cbs = []
        for i in range(10):
            cb = CheckBox(active=True)
            self.bai_cbs.append(cb)
            bai_grid.add_widget(cb)
            bai_grid.add_widget(Label(text=str(i), font_size=14))
        root.add_widget(bai_grid)
        
        root.add_widget(Label(text='十位', font_size=14))
        shi_grid = GridLayout(cols=5, spacing=10)
        self.shi_cbs = []
        for i in range(10):
            cb = CheckBox(active=True)
            self.shi_cbs.append(cb)
            shi_grid.add_widget(cb)
            shi_grid.add_widget(Label(text=str(i), font_size=14))
        root.add_widget(shi_grid)
        
        root.add_widget(Label(text='个位', font_size=14))
        wei_grid = GridLayout(cols=5, spacing=10)
        self.wei_cbs = []
        for i in range(10):
            cb = CheckBox(active=True)
            self.wei_cbs.append(cb)
            wei_grid.add_widget(cb)
            wei_grid.add_widget(Label(text=str(i), font_size=14))
        root.add_widget(wei_grid)
        
        action_btns = BoxLayout(spacing=15)
        action_btns.add_widget(Button(text='开始缩水', on_press=self.run_filter, size_hint=(0.6, 1), font_size=18))
        action_btns.add_widget(Button(text='重置', on_press=self.reset_all, size_hint=(0.4, 1), font_size=18))
        root.add_widget(action_btns)
        
        self.count_label = Label(text='剩余注数: 1000', font_size=18, bold=True)
        root.add_widget(self.count_label)
        
        self.result_scroll = ScrollView(size_hint=(1, 0.3))
        self.result_label = Label(text='', font_size=14, size_hint_y=None)
        self.result_scroll.add_widget(self.result_label)
        root.add_widget(self.result_scroll)
        
        return root
    
    def select_all_danma(self, instance):
        for cb in self.danma_cbs:
            cb.active = True
    
    def clear_all_danma(self, instance):
        for cb in self.danma_cbs:
            cb.active = False
    
    def run_filter(self, instance):
        danma = [i for i, cb in enumerate(self.danma_cbs) if cb.active]
        tails = [i for i, cb in enumerate(self.tail_cbs) if cb.active]
        spans = [i for i, cb in enumerate(self.span_cbs) if cb.active]
        bai = [i for i, cb in enumerate(self.bai_cbs) if cb.active]
        shi = [i for i, cb in enumerate(self.shi_cbs) if cb.active]
        wei = [i for i, cb in enumerate(self.wei_cbs) if cb.active]
        
        results = []
        for ticket in ALL_TICKETS:
            if danma and not any(d in danma for d in ticket.digits):
                continue
            if tails and ticket.sum() % 10 not in tails:
                continue
            if spans and ticket.span() not in spans:
                continue
            if bai and ticket.bai not in bai:
                continue
            if shi and ticket.shi not in shi:
                continue
            if wei and ticket.wei not in wei:
                continue
            results.append(ticket)
        
        self.count_label.text = f'剩余注数: {len(results)}'
        
        if not results:
            self.result_label.text = '没有符合条件的号码'
        else:
            lines = [f"{t.num:03d}" for t in results]
            formatted = []
            for i in range(0, len(lines), 4):
                formatted.append(' '.join(lines[i:i+4]))
            self.result_label.text = '\n'.join(formatted)
        self.result_label.height = max(self.result_label.texture_size[1], 100)
    
    def reset_all(self, instance):
        for cb in self.danma_cbs:
            cb.active = True
        for cb in self.tail_cbs:
            cb.active = True
        for cb in self.span_cbs:
            cb.active = True
        for cb in self.bai_cbs:
            cb.active = True
        for cb in self.shi_cbs:
            cb.active = True
        for cb in self.wei_cbs:
            cb.active = True
        self.count_label.text = '剩余注数: 1000'
        lines = [f"{i:03d}" for i in range(1000)]
        formatted = []
        for i in range(0, len(lines), 4):
            formatted.append(' '.join(lines[i:i+4]))
        self.result_label.text = '\n'.join(formatted)
        self.result_label.height = max(self.result_label.texture_size[1], 100)

if __name__ == '__main__':
    FilterApp().run()
