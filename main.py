import subprocess
import sys

from PyQt5 import QtWidgets

from ui import mw


class MW(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = mw.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.send_btn.clicked.connect(self.send)

    def send(self):
        """ основной метод отправки """

        #  Получаем  общую информацию
        server = self.ui.server_ip_le.text()
        port = self.ui.server_port_le.text()
        end_of_track = 'true' if self.ui.eot_check.isChecked() else 'false'
        track_id = self.ui.track_id_le.text()
        camera_id = self.ui.cam_id_le.text()
        #  Получаем перрвый трек
        first_ts = self.ui.first_ts_dte.dateTime().toPyDateTime().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        first_bbox = self.bbox_convert(self.ui.first_bbox_le.text())
        first_quality = self.ui.first_qual_le.text()
        #  Получаем последний трек
        last_ts = self.ui.last_ts_dte.dateTime().toPyDateTime().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        last_bbox = self.bbox_convert(self.ui.last_bbox_le.text())
        last_quality = self.ui.last_qual_le.text()
        #  Получаем лучший трек
        best_ts = self.ui.best_ts_dte.dateTime().toPyDateTime().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        best_bbox = self.bbox_convert(self.ui.best_bbox_le.text())
        best_quality = self.ui.best_qual_le.text()
        #  Получаем историю
        history_bbox = self.bbox_sequence_convert(self.ui.history_bbox_le.text())
        history_active_tracks = self.bbox_convert(self.ui.history_at_le.text())

        message = {
          "cam_id": camera_id,
          "end_of_track": end_of_track,
          "track_duration_seconds": 1,
          "track": {
            "id": track_id,
            "body": {
              "first": {
                "timestamp": first_ts,
                "bbox": first_bbox,
                "quality": first_quality,
                "full_frame": "multipart:photo_first"},
              "last": {
                "timestamp": last_ts,
                "bbox": last_bbox,
                "quality": last_quality,
                "full_frame": "multipart:photo_last"},
              "best": {
                "timestamp": best_ts,
                "bbox": best_bbox,
                "quality": best_quality,
                "full_frame": "multipart:photo_best",
                "normalized": "multipart:photo_normalized"},
              "history": {
                "first_timestamp": first_ts,
                "last_timestamp": last_ts,
                "bbox": history_bbox,
                "active_tracks": history_active_tracks}
            }
          }
        }

        request = f'curl --request POST --url http://{server}:{port}/sending --header \'Content-Type: multipart/form-data\' --header \'content-type: multipart/form-data; boundary=---011000010111000001101001\' --form \'message={message}\' --form photo_first=@001.jpg --form photo_last=@001.jpg --form photo_best=@001.jpg --form photo_normalized=@001.jpg --form topic=silhouette --form count=3 --form delay=4'

        res = subprocess.getoutput(request)

    @staticmethod
    def bbox_convert(data: str) -> str:
        """
            конвертим bbox
        :param data: входные данные строки
        :return: лист bbox'ов в строку для запроса
        """

        return str(data.split(',')).replace('\'', '')

    def bbox_sequence_convert(self, data: str) -> str:
        """
            конвертим последовательность bbox'ов
        :param data: входные данные строки
        :return: лист bbox'ов в строку для запроса
        """

        temp = data.split(';')
        result_list = []
        for item in temp:
            result_list.append(self.bbox_convert(item))

        return str(result_list).replace('\'', '')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MW()
    application.show()

    sys.exit(app.exec())
