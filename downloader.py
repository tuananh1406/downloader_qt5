# coding: utf-8
import sys
import os
import urllib.request

import pafy
import humanize

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUiType


GIAO_DIEN, _ = loadUiType('downloader.ui')


class ChuongTrinhChinh(QMainWindow, GIAO_DIEN):

    '''
    Chương trình tải video từ đường dẫn youtube
    '''

    def __init__(self, parent=None):
        super(ChuongTrinhChinh, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.khoi_tao_ui()
        self.nhan_nut()

    def khoi_tao_ui(self):
        '''
        Khởi tạo thay đổi trên giao diện chương trình
        '''

    def nhan_nut(self):
        '''
        Xử lý khi ấn nút
        '''
        # Các xử lý chức năng tải tệp bất kỳ
        self.tai_xuong.clicked.connect(self.bat_dau_tai)
        self.chon_noi_luu.clicked.connect(self.duyet_tep)

        # Các xử lý của chức năng tải video đơn từ Youtube
        self.kiem_tra_video_don.clicked.connect(self.lay_du_lieu_video)
        self.duyet_tep_video_don.clicked.connect(self.duyet_video_don)
        self.tai_xuong_video_don.clicked.connect(self.tai_video_don)

        # Các xử lý của chức năng tải video theo danh sách phát
        self.kiem_tra_danh_sach.clicked.connect(self.lay_thong_tin_danh_sach)
        self.duyet_tep_danh_sach.clicked.connect(self.duyet_danh_sach)
        self.tai_xuong_danh_sach.clicked.connect(self.tai_video_danh_sach)

    def tien_trinh_tai(self, blocknum, blocksize, totalsize):
        '''
        Tính toán tiến trình tải xuống
        '''
        dung_luong_noi_dung = blocknum * blocksize
        if totalsize > 0:
            ti_le = dung_luong_noi_dung * 100 / totalsize
            self.thanh_tien_trinh.setValue(ti_le)
            QApplication.processEvents()

    def duyet_tep(self):
        '''
        Duyệt tệp tin trong máy tính
        '''
        duong_dan_luu = QFileDialog.getSaveFileName(
            self,
            caption='Chọn nơi lưu',
            directory='.',
            filter="All files(*.*)",
            )
        self.duong_dan_luu.setText(duong_dan_luu[0])

    def bat_dau_tai(self):
        '''
        Tải tệp vào máy tính
        '''
        thong_tin_tai = self.duong_dan_tai.text()
        thong_tin_luu = self.duong_dan_luu.text()

        if thong_tin_tai == '' or thong_tin_luu == '':
            QMessageBox.warning(
                    self,
                    "Sai thông tin",
                    'Vui lòng kiểm tra lại đường dẫn tải và đường dẫn lưu',
                    )
        else:
            try:
                urllib.request.urlretrieve(
                        thong_tin_tai,
                        thong_tin_luu,
                        self.tien_trinh_tai,
                        )
            except Exception as e:
                QMessageBox(self, 'Có lỗi xảy ra', e)
                return
        QMessageBox.information(self, 'Tải xuống thành công', 'Đã tải xong!')
        self.duong_dan_tai.setText('')
        self.duong_dan_luu.setText('')
        self.thanh_tien_trinh.setValue(0)

    # Tải video đơn trên Youtube
    def lay_du_lieu_video(self):
        '''
        Lấy thông tin về video
        '''
        duong_dan_tai = self.duong_dan_video_don.text()
        if duong_dan_tai == '':
            QMessageBox.warning(
                    self,
                    'Lỗi dữ liệu',
                    'Thông tin đường dẫn không chính xác',
                    )
        else:
            video = pafy.new(duong_dan_tai)
            tieu_de = video.title
            thoi_luong = video.duration
            nguoi_dang = video.author
            luot_xem = video.viewcount
            luot_like = video.likes
            luot_dislike = video.dislikes
            thong_tin = [
                    'Thông tin video:\n',
                    'Tiêu đề: %s\n' % (tieu_de),
                    'Thời lượng: %s\n' % (thoi_luong),
                    'Người đăng: %s\n' % (nguoi_dang),
                    'Lượt xem: %s\n' % (luot_xem),
                    'Lượt like: %s\n' % (luot_like),
                    'Lượt dislike: %s\n' % (luot_dislike),
                    ]
            QMessageBox.information(
                    self,
                    'Thông tin video',
                    '\n'.join(thong_tin),
                    )
            du_lieu_video = video.videostreams
            for thong_tin_video in du_lieu_video:
                dung_luong = thong_tin_video.get_filesize()
                ds_do_phan_giai = '%s - %s - %s - %s' % (
                        thong_tin_video.mediatype,
                        thong_tin_video.extension,
                        thong_tin_video.quality,
                        humanize.naturalsize(dung_luong),
                        )
                self.chat_luong_video_don.addItem(ds_do_phan_giai)

    def duyet_video_don(self):
        '''
        Chọn nơi lưu video đơn
        '''
        duong_dan_luu = QFileDialog.getSaveFileName(
            self,
            caption='Chọn nơi lưu',
            directory='.',
            filter="All files(*.*)",
            )
        self.noi_luu_video_don.setText(duong_dan_luu[0])

    def tai_video_don(self):
        '''
        Tải video về máy
        '''
        duong_dan_luu = self.noi_luu_video_don.text()
        duong_dan_tai = self.duong_dan_video_don.text()
        if duong_dan_tai == '' or duong_dan_luu == '':
            QMessageBox.warning(
                    self,
                    'Lỗi dữ liệu',
                    'Thông tin đường dẫn không chính xác',
                    )
        else:
            video = pafy.new(duong_dan_tai)
            thong_tin_video = video.videostreams
            chat_luong = self.chat_luong_video_don.currentIndex()
            thong_tin_video[chat_luong].download(
                    filepath=duong_dan_luu,
                    callback=self.tien_trinh_tai_video_don,
                    )

    def tien_trinh_tai_video_don(self, total, received, ratio, rate, time):
        '''
        Hiển thị tiến trình tải video
        '''
        da_tai_duoc = received
        if total > 0:
            ti_le = da_tai_duoc * 100 / total
            self.tien_trinh_video_don.setValue(ti_le)
            thoi_gian_con_lai = round(time / 60, 2)
            self.thoi_gian_video_don.setText(
                    '%s phút còn lại' % (thoi_gian_con_lai)
                    )
            QApplication.processEvents()

    # Tải video theo danh sách
    def lay_thong_tin_danh_sach(self):
        '''
        Lấy thông tin của danh sách phát
        '''
        duong_dan_tai = self.duong_dan_danh_sach.text()
        if duong_dan_tai == '':
            QMessageBox.warning(
                    self,
                    'Lỗi khi tải video',
                    'Đường dẫn tải video hoặc nơi lưu không chính xác!',
                    )
        else:
            danh_sach_phat = pafy.get_playlist(duong_dan_tai)
            danh_sach_video = danh_sach_phat['items']
            self.tong_so_video.display(len(danh_sach_video))
            # Lấy danh sách độ phân giải
            ds_chat_luong = []
            for stt, video in enumerate(danh_sach_video):
                ds_do_phan_giai = video['pafy'].videostreams
                QApplication.processEvents()
                for do_phan_giai in ds_do_phan_giai:
                    self.lay_danh_sach_phat.setText(
                            'Lấy thông tin video thứ %s' % (stt + 1),
                            )
                    if str(do_phan_giai.quality) not in ds_chat_luong:
                        ds_chat_luong.append(str(do_phan_giai.quality))
            for chat_luong in ds_chat_luong:
                self.chat_luong_danh_sach.addItem(chat_luong)

    def duyet_danh_sach(self):
        '''
        Chọn nơi lưu danh sách video
        '''
        duong_dan_luu = QFileDialog.getExistingDirectory(
            self,
            caption='Chọn nơi lưu',
            directory='.',
            )
        self.duong_dan_luu_danh_sach.setText(duong_dan_luu)

    def tai_video_danh_sach(self):
        '''
        Tải video theo danh sách phát
        '''
        duong_dan_tai = self.duong_dan_danh_sach.text()
        duong_dan_luu = self.duong_dan_luu_danh_sach.text()
        if duong_dan_tai == '' or duong_dan_luu == '':
            QMessageBox.warning(
                    self,
                    'Lỗi khi tải video',
                    'Đường dẫn tải video hoặc nơi lưu không chính xác!',
                    )
        else:
            danh_sach_phat = pafy.get_playlist(duong_dan_tai)
            thu_muc_goc = os.path.join(duong_dan_luu, danh_sach_phat['title'])
            if not os.path.exists(thu_muc_goc):
                os.mkdir(thu_muc_goc)
            chat_luong_video = self.chat_luong_danh_sach.currentIndex()
            for stt, video in enumerate(danh_sach_phat['items']):
                video_hien_tai = video['pafy']
                tai_video = video_hien_tai.videostreams
                self.video_hien_tai.display(stt + 1)
                QApplication.processEvents()
                tai_video[chat_luong_video].download(
                        filepath=thu_muc_goc,
                        callback=self.tien_trinh_danh_sach,
                        )

    def tien_trinh_danh_sach(self, total, received, ratio, rate, time):
        '''
        Tiến trình khi tải video theo danh sách phát
        '''
        da_tai_duoc = received
        if total > 0:
            ti_le = da_tai_duoc * 100 / total
            self.tien_trinh_tai_danh_sach.setValue(ti_le)
            thoi_gian_con_lai = round(time / 60, 2)
            self.lay_danh_sach_phat.setText(
                    '%s phút còn lại' % (thoi_gian_con_lai)
                    )
            QApplication.processEvents()


def main():
    '''
    Hàm chạy chương trình
    '''
    chuong_trinh = QApplication(sys.argv)
    cua_so = ChuongTrinhChinh()
    cua_so.show()
    chuong_trinh.exec_()


if __name__ == '__main__':
    main()
