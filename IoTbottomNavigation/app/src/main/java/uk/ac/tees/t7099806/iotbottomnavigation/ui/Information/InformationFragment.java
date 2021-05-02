package uk.ac.tees.t7099806.iotbottomnavigation.ui.Information;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.w3c.dom.Text;

import java.util.concurrent.ExecutionException;

import uk.ac.tees.t7099806.iotbottomnavigation.MainActivity;
import uk.ac.tees.t7099806.iotbottomnavigation.R;
import uk.ac.tees.t7099806.iotbottomnavigation.SettingsActivity;

public class InformationFragment extends Fragment implements View.OnClickListener {

    Button settingsBtn, releaseBtn;

    String clientId;
    MqttAndroidClient client;
    private String USERNAME = "ferg";
    private String PASSWORD = "pass";

    MqttConnectOptions options;

    TextView cameraOn, feedAmount;

    String store;
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        View root = inflater.inflate(R.layout.fragment_information, container, false);

        settingsBtn = root.findViewById(R.id.buttonChangeSettings);
        settingsBtn.setOnClickListener(this);

        releaseBtn = root.findViewById(R.id.buttonReleaseFood);
        releaseBtn.setOnClickListener(this);

        clientId = MqttClient.generateClientId();
        client =
                new MqttAndroidClient(getContext(), "tcp://broker.hivemq.com:1883",
                        clientId);

        MqttConnectOptions options = new MqttConnectOptions();
        options.setUserName(USERNAME);
        options.setPassword(PASSWORD.toCharArray());

        cameraOn =  root.findViewById(R.id.cameraOn);
        feedAmount = root.findViewById(R.id.feedAmount);

        try {
            IMqttToken token = client.connect(options);
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {

                    subscribe("/petprotector/feeder_actuator", feedAmount);
                    subscribe("/petprotector/camera_actuator", cameraOn);

//                    subscribe("/petprotector/feeder_actuator/feeding_times");
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Toast.makeText(getContext(), "Failure", Toast.LENGTH_SHORT).show();
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }


       // petTemp.setText(store);
        Toast.makeText(getContext(), store, Toast.LENGTH_SHORT).show();

        return root;
    }

    @Override
    public void onClick(View v) {
        if(v == settingsBtn)
        {
            startActivity(new Intent(getContext(), SettingsActivity.class));
        }
        if(v == releaseBtn)
        {

        }
    }



    private void subscribe(String channelName, TextView t)
    {
        try{
            if(client.isConnected())
            {
                client.subscribe("/petprotector/camera_actuator", 0);
                client.subscribe("/petprotector/feeder_actuator", 0);
                client.setCallback(new MqttCallback() {
                    @Override
                    public void connectionLost(Throwable cause) {

                    }

                    @Override
                    public void messageArrived(String topic, MqttMessage message) throws Exception {
                        if(topic.equals("/petprotector/camera_actuator"))
                        {
                            cameraOn.setText(message.toString());
                        }
                        else if (topic.equals("/petprotector/feeder_actuator"))
                        {
                            feedAmount.setText(message.toString());
                        }

                    }

                    @Override
                    public void deliveryComplete(IMqttDeliveryToken token) {

                    }
                });
            }
        } catch (Exception e){
            Log.d("tag", "Error: " + e);
        }
    }


}