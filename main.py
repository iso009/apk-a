from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest
import json

CURRENT_VERSION = "1.0.1"
VERSION_CHECK_URL = "https://raw.githubusercontent.com/iso009/apk-a/main/version.json"

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
        self.spacing = 8
        self.size_hint_y = None
        self.height = 150
        
        self.add_widget(Label(text='财富广场彩票站', font_size=16, color=(1, 0, 0, 1), size_hint_y=None, height=30))
        self.add_widget(Label(text='微信: 13296999092', font_size=14, color=(1, 0, 0, 1), size_hint_y=None, height=25))
        
        title = Label(text='定胆号码', font_size=18, bold=True, size_hint_y=None, height=30)
        self.add_widget(title)
        
        grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=40)
        self.checkboxes = []
        for i in range(10):
            cb = CheckBox(active=True, size_hint=(None, None), size=(35, 35))
            self.checkboxes.append(cb)
            grid.add_widget(cb)
            grid.add_widget(Label(text=str(i), font_size=14))
        self.add_widget(grid)
        
        btn_layout = BoxLayout(spacing=10, size_hint_y=None, height=40)
        self.select_all_btn = Button(text='全选', size_hint=(0.5, 1), font_size=14)
        self.select_all_btn.bind(on_press=self.select_all)
        self.clear_btn = Button(text='清空', size_hint=(0.5, 1), font_size=14)
        self.clear_btn.bind(on_press=self.clear_all)
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
        self.spacing = 8
        self.size_hint_y = None
        self.height = 160
        
        title = Label(text='和值/跨度', font_size=18, bold=True, size_hint_y=None, height=30)
        self.add_widget(title)
        
        self.add_widget(Label(text='和尾:', font_size=14, size_hint_y=None, height=25))
        tail_grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=35)
        self.tail_checkboxes = []
        for i in range(10):
            cb = CheckBox(active=True, size_hint=(None, None), size=(30, 30))
            self.tail_checkboxes.append(cb)
            tail_grid.add_widget(cb)
            tail_grid.add_widget(Label(text=str(i), font_size=12))
        self.add_widget(tail_grid)
        
        self.add_widget(Label(text='跨度:', font_size=14, size_hint_y=None, height=25))
        span_grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=35)
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
        self.spacing = 8
        self.size_hint_y = None
        self.height = 220
        
        title = Label(text='定位胆码', font_size=18, bold=True, size_hint_y=None, height=30)
        self.add_widget(title)
        
        self.add_widget(Label(text='百位:', font_size=14, size_hint_y=None, height=25))
        bai_grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=35)
        self.bai_checkboxes = []
        for i in range(10):
            cb = CheckBox(active=True, size_hint=(None, None), size=(30, 30))
            self.bai_checkboxes.append(cb)
            bai_grid.add_widget(cb)
            bai_grid.add_widget(Label(text=str(i), font_size=12))
        self.add_widget(bai_grid)
        
        self.add_widget(Label(text='十位:', font_size=14, size_hint_y=None, height=25))
        shi_grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=35)
        self.shi_checkboxes = []
        for i in range(10):
            cb = CheckBox(active=True, size_hint=(None, None), size=(30, 30))
            self.shi_checkboxes.append(cb)
            shi_grid.add_widget(cb)
            shi_grid.add_widget(Label(text=str(i), font_size=12))
        self.add_widget(shi_grid)
        
        self.add_widget(Label(text='个位:', font_size=14, size_hint_y=None, height=25))
        wei_grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=35)
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

class FilterApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = BoxLayout(size_hint_y=None, height=50, spacing=10)
        header.add_widget(Label(text=f'版本: {CURRENT_VERSION}', font_size=14))
        self.update_btn = Button(text='检查更新', size_hint=(0.4, 1), font_size=14)
        self.update_btn.bind(on_press=self.check_update)
        header.add_widget(self.update_btn)
        self.root.add_widget(header)
        
        main_scroll = ScrollView(size_hint=(1, 0.55))
        main_content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        main_content.bind(minimum_height=main_content.setter('height'))
        
        self.danma_panel = DanmaPanel()
        main_content.add_widget(self.danma_panel)
        
        self.sum_span_panel = SumSpanPanel()
        main_content.add_widget(self.sum_span_panel)
        
        self.position_panel = PositionPanel()
        main_content.add_widget(self.position_panel)
        
        self.filter_btn = Button(text='开始缩水', size_hint=(1, None), height=60, font_size=20)
        self.filter_btn.bind(on_press=self.run_filter)
        main_content.add_widget(self.filter_btn)
        
        self.reset_btn = Button(text='重置条件', size_hint=(1, None), height=50, font_size=16)
        self.reset_btn.bind(on_press=self.reset_conditions)
        main_content.add_widget(self.reset_btn)
        
        self.count_label = Label(text='剩余注数: 1000', font_size=16, size_hint=(1, None), height=40)
        main_content.add_widget(self.count_label)
        
        main_scroll.add_widget(main_content)
        self.root.add_widget(main_scroll)
        
        self.result_scroll = ScrollView(size_hint=(1, 0.4))
        self.result_label = Label(text='', font_size=14, size_hint_y=None)
        self.result_scroll.add_widget(self.result_label)
        self.root.add_widget(self.result_scroll)
        
        self.check_update(None)
        
        return self.root
    
    def check_update(self, instance):
        try:
            UrlRequest(VERSION_CHECK_URL, on_success=self.on_version_check, on_failure=self.on_version_fail)
        except:
            if instance:
                self.show_popup('提示', '网络连接失败')
    
    def on_version_check(self, req, result):
        try:
            latest_version = result.get('version', CURRENT_VERSION)
            download_url = result.get('download_url', '')
            
            if latest_version > CURRENT_VERSION:
                content = BoxLayout(orientation='vertical', padding=10, spacing=10)
                content.add_widget(Label(text=f'发现新版本: {latest_version}', font_size=16))
                content.add_widget(Label(text='点击确定开始下载更新', font_size=14))
                popup = Popup(title='版本更新', content=content, size_hint=(0.8, 0.5))
                update_btn = Button(text='确定', size_hint=(1, None), height=50)
                update_btn.bind(on_press=lambda x: self.download_update(download_url, popup))
                content.add_widget(update_btn)
                popup.open()
            else:
                if self.update_btn:
                    self.show_popup('提示', '当前已是最新版本')
        except:
            pass
    
    def on_version_fail(self, req, error):
        pass
    
    def download_update(self, url, popup):
        popup.dismiss()
        self.show_popup('提示', '正在下载更新，请稍后...')
        try:
            import webbrowser
            webbrowser.open(url)
        except:
            self.show_popup('提示', '请手动下载更新')
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_btn = Button(text='确定', size_hint=(1, None), height=40)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        popup.open()
    
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
        
        if not results:
            self.result_label.text = '没有符合条件的号码'
        else:
            lines = [f"{t.num:03d}" for t in results]
            formatted = []
            for i in range(0, len(lines), 5):
                formatted.append(' '.join(lines[i:i+5]))
            self.result_label.text = '\n'.join(formatted)
        self.result_label.height = max(self.result_label.texture_size[1], 100)
    
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
        lines = [f"{i:03d}" for i in range(1000)]
        formatted = []
        for i in range(0, len(lines), 5):
            formatted.append(' '.join(lines[i:i+5]))
        self.result_label.text = '\n'.join(formatted)
        self.result_label.height = max(self.result_label.texture_size[1], 100)

if __name__ == '__main__':
    FilterApp().run()
