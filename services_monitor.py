#coding=utf-8
import json
import tornado.ioloop
import tornado.web
import torndb
import os
import string

#*/1 * * * * sh /usr/local/services/spider_task_center/tools/run_spider_task_center.sh &
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("linechart.html", title="Spider Task Center", items=items)

class InterfaceHandler(tornado.web.RequestHandler):
    def get(self):
        day = self.get_argument("day")
        if not day:
            self.write(403)
        interface_list = ["listProductFeeds", "myProductFeeds", "listNewQuestion", "getQuestionDetail", \
                          "search", "getProductInfo", "getProductInfoById", "getRelatedQuestionByProduct",\
                          "listProductsByCategory"]
        visit_filename_list = []
        cost_filename_list = []
        for i in range(0, len(interface_list)):
            visit_filename_list.append("/static/" + str(interface_list[i]) + "_visit_" + day +".tsv")
            cost_filename_list.append("/static/" + str(interface_list[i]) + "_cost_" + day +".tsv")
        self.render("interface.html", \
                    interface_list = interface_list, \
                    visit_filename_list = visit_filename_list, \
                    cost_filename_list = cost_filename_list, \
                    y_desc_visit = "个", \
                    y_desc_cost = "毫秒")

class InterfaceCostHandler(tornado.web.RequestHandler):
    def get(self):
        interface_name = self.get_argument("interface_name")
        day = self.get_argument("day")
        if (not interface_name) or (not day):
            self.write(403)
        data_filename = "/static/" + str(interface_name) + "_cost_" + day +".tsv"
        self.render("interface.html", \
                    interface_name = "interface avg cost[" + str(interface_name) + "][" + data_filename + "]", \
                    data_filename=data_filename, \
                    y_desc = "毫秒")

class InterfaceVisitHandler(tornado.web.RequestHandler):
    def get(self):
        interface_name = self.get_argument("interface_name")
        day = self.get_argument("day")
        if (not interface_name) or (not day):
            self.write(403)
        data_filename = "/static/" + str(interface_name) + "_visit_" + day +".tsv"
        self.render("interface.html", \
                    interface_name = "interface visit count[" +str(interface_name) + "][" + data_filename + "]", \
                    data_filename=data_filename, \
                    y_desc = "个")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "data"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/interface/cost", InterfaceCostHandler),
    (r"/interface/visit", InterfaceVisitHandler),
    (r"/interface", InterfaceHandler),
    #(r"/(data\.tsv)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], **settings)

if __name__ == "__main__":
    application.listen(8899)
    tornado.ioloop.IOLoop.instance().start()
