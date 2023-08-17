# hotbot_app/forms.py

from django import forms

class BotConfigForm(forms.Form):
    price = forms.DecimalField(label='Price', required=True)
    currency = forms.ChoiceField(label='Currency', choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum')], required=True)
    bot_run_time = forms.IntegerField(label='Run Time', required=True)  # Change the field name to match the one used in the views.py file
    desired_ROI = forms.DecimalField(label='Desired ROI', required=True)
    stop_loss = forms.DecimalField(label='Stop Loss', required=True)
