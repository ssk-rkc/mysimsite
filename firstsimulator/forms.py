from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class ImportDataForm(forms.Form):
    Time_PV_MV = forms.FileField(
        required = True,
        label="システム同定するcsvデータ",
        initial="./firstsimulator/data/Time_PVMV_tf2.csv",
        help_text="Time[s],PV[℃],MV[%]の順に並んだcsvファイルを指定してください"
    )
    data_Sampling_Time = forms.FloatField(
        label="データサンプリング時間　[s]",
        validators=[MinValueValidator(0.001), MaxValueValidator(10)],
        initial=10,
        help_text=" 読み込むデータのサンプリング時間を入力してください (0.1~10)"
    )
    Number_Of_Data = forms.IntegerField(
        label="システム同定に使用するデータ数",
        validators=[MinValueValidator(50), MaxValueValidator(1000)],
        initial=300,
        help_text="(50~1000)"
    )

class PidSettingParameterForm(forms.Form):
    SV = forms.IntegerField(
        label="設定温度　: SV",
        validators = [MinValueValidator(10), MaxValueValidator(400)],
        initial = 120,
        help_text = "[℃]"
    )
    P = forms.IntegerField(
        label="比例帯 　:　P",
        validators = [MinValueValidator(0), MaxValueValidator(400)],
        initial = 30,
        help_text = "[℃]"
    )
    I = forms.IntegerField(
        label="積分時間　:  Ti",
        validators = [MinValueValidator(0), MaxValueValidator(3600)],
        initial = 240,
        help_text = "[s]"
    )
    D = forms.IntegerField(
        label="微分時間　: Td",
        validators = [MinValueValidator(0), MaxValueValidator(400)],
        initial = 60,
        help_text = "[s]"
    )
    eta = forms.IntegerField(
        label="微分ゲイン :DG",
        validators = [MinValueValidator(0), MaxValueValidator(400)],
        initial = 4,
        widget=forms.HiddenInput()
    )
    ARW = forms.ChoiceField(
        label="リセットワインドアップ対策",
        widget=forms.widgets.Select,
        choices = (
            ('0', "なし"),
            ('1', "ARW")
        )
    )

class PlantSettingParameterForm(forms.Form):
    #システム同定結果の係数を取り込みたい
    coef1 = forms.FloatField(
        label="係数　a0",
        initial=0.005,
#        disabled=True

    )
    coef2 = forms.FloatField(
        label="係数　a1",
        initial=0.52,
#        disabled=True
    )
    coef3 = forms.FloatField(
        label="係数　b0",
        initial=0.01,
#        readonly=True
    )
    coef = [coef1, coef2, coef3]
    PGain = 1

class SimSettingParameterForm(forms.Form):
    StopTime = forms.IntegerField(
        label="シミュレーション終了時間 [s]",
        validators=[MinValueValidator(10), MaxValueValidator(1000)],
        initial=300,
        help_text="10~1000"
    )
    SampleTime = forms.IntegerField(
        label="シミュレーション時間刻み　[s]",
        validators=[MinValueValidator(0.1), MaxValueValidator(10)],
        initial=1,
        help_text="0.1~10"

    )


