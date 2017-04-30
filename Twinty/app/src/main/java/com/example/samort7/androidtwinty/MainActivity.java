package com.example.samort7.androidtwinty;

import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.telephony.PhoneNumberFormattingTextWatcher;
import android.telephony.PhoneNumberUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.util.Locale;


public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        Button button1 = (Button) findViewById(R.id.button);
        button1.setOnClickListener(this);
        Button button2 = (Button) findViewById(R.id.button2);
        button2.setOnClickListener(this);

        EditText inputField = (EditText) findViewById(R.id.editText);
        inputField.addTextChangedListener(new PhoneNumberFormattingTextWatcher());

    }

    @Override
    public void onClick(View b) {
        Context context = getApplicationContext();
        switch (b.getId()) {
            case R.id.button:
                Toast.makeText(context, "I am button 1! Yaaay!", Toast.LENGTH_LONG).show();
                break;
            case R.id.button2:
                Toast.makeText(context, "Button 2 is the best!", Toast.LENGTH_LONG).show();
                break;
        }
    }
}
