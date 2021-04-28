package uk.ac.tees.t7099806.iotbottomnavigation.ui.Information;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import uk.ac.tees.t7099806.iotbottomnavigation.R;
import uk.ac.tees.t7099806.iotbottomnavigation.SettingsActivity;

public class InformationFragment extends Fragment implements View.OnClickListener {

    Button settingsBtn;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        View root = inflater.inflate(R.layout.fragment_information, container, false);

        settingsBtn = root.findViewById(R.id.buttonChangeSettings);
        settingsBtn.setOnClickListener(this);

        return root;
    }

    @Override
    public void onClick(View v) {
        if(v == settingsBtn)
        {
            startActivity(new Intent(getActivity(), SettingsActivity.class));
        }
    }
}