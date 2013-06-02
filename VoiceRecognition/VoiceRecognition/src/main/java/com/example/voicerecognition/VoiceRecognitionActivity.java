package com.example.voicerecognition;

import java.io.*;
import java.net.URLEncoder;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.lang.String;

import android.annotation.TargetApi;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;

public class VoiceRecognitionActivity extends Activity {

    private static final int VOICE_RECOGNITION_REQUEST_CODE = 1001;

    private ListView mlvTextMatches;
    private Button mbtSpeak;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_voice_recognition);
        mlvTextMatches = (ListView) findViewById(R.id.lvTextMatches);
        mbtSpeak = (Button) findViewById(R.id.btSpeak);
        checkVoiceRecognition();
    }

    String combine(ArrayList<java.lang.String> s, String glue)
    {
        int k=s.size();
        if (k==0)
            return null;
        StringBuilder out=new StringBuilder();
        out.append(s.get(0));
        for (int x=1;x<k;++x)
            out.append(glue).append(s.get(x));
        return out.toString();
    }

    public void checkVoiceRecognition() {
        // Check if voice recognition is present
        PackageManager pm = getPackageManager();
        List<android.content.pm.ResolveInfo> activities = pm.queryIntentActivities(new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH), 0);
        if (activities.size() == 0) {
            mbtSpeak.setEnabled(false);
            mbtSpeak.setText("Voice recognizer not present");
            Toast.makeText(this, "Voice recognizer not present",Toast.LENGTH_SHORT).show();
        }
    }

    public void sendMsgToServer(ArrayList<java.lang.String> aStrings){

        String url = "http://192.168.0.6/Sender/XbeeWrapper.php?iCmdType=CMD_SPEAK&iCmdStrings=";
        String aCmd = combine(aStrings,"_");
        url = url + aCmd;
        url = url.replace(' ','-');
        url = Normalizer.normalize(url, Normalizer.Form.NFD);
        url = url.replaceAll("[^\\p{ASCII}]", "");
        grabURL(url);
    }

    public void grabURL(String url) {
        new GrabURL().execute(url);
    }

    public void speak(View view) {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);

        // Specify the calling package to identify your application
        intent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, getClass().getPackage().getName());

        // Given an hint to the recognizer about what the user is going to say
        //There are two form of language model available
        //1.LANGUAGE_MODEL_WEB_SEARCH : For short phrases
        //2.LANGUAGE_MODEL_FREE_FORM  : If not sure about the words or phrases and its domain.
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_WEB_SEARCH);

        // Specify how many results you want to receive. The results will be sorted where the first result is the one with higher confidence.
        int noOfMatches = 4;
        intent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, noOfMatches);
        //Start the Voice recognizer activity for the result.
        startActivityForResult(intent, VOICE_RECOGNITION_REQUEST_CODE);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == VOICE_RECOGNITION_REQUEST_CODE)

            //If Voice recognition is successful then it returns RESULT_OK
            if(resultCode == RESULT_OK) {

                ArrayList<java.lang.String> textMatchList = data
                        .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);

                if (!textMatchList.isEmpty()) {
                    mlvTextMatches
                            .setAdapter(new ArrayAdapter<java.lang.String>(this,
                                    android.R.layout.simple_list_item_1,
                                    textMatchList));
                    sendMsgToServer(textMatchList);

                }
                //Result code for various error.
            }else if(resultCode == RecognizerIntent.RESULT_AUDIO_ERROR){
                showToastMessage("Audio Error");
            }else if(resultCode == RecognizerIntent.RESULT_CLIENT_ERROR){
                showToastMessage("Client Error");
            }else if(resultCode == RecognizerIntent.RESULT_NETWORK_ERROR){
                showToastMessage("Network Error");
            }else if(resultCode == RecognizerIntent.RESULT_NO_MATCH){
                showToastMessage("No Match");
            }else if(resultCode == RecognizerIntent.RESULT_SERVER_ERROR){
                showToastMessage("Server Error");
            }
        super.onActivityResult(requestCode, resultCode, data);
    }
    /**
     * Helper method to show the toast message
     **/
    void showToastMessage(String message){
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }


    private class GrabURL extends AsyncTask<String, Void, Void> {
        private final HttpClient Client = new DefaultHttpClient();
        private String Content;
        private String Error = null;
        private ProgressDialog Dialog = new ProgressDialog(VoiceRecognitionActivity.this);

        protected void onPreExecute() {
            Dialog.setMessage("Downloading source..");
            Dialog.show();
        }

        protected Void doInBackground(String... urls) {
            try {
                HttpGet httpget = new HttpGet(urls[0]);
                ResponseHandler<String> responseHandler = new BasicResponseHandler();
                Content = Client.execute(httpget, responseHandler);
            } catch (ClientProtocolException e) {
                Error = e.getMessage();
                cancel(true);
            } catch (IOException e) {
                Error = e.getMessage();
                cancel(true);
            }

            return null;
        }

        protected void onPostExecute(Void unused) {
            Dialog.dismiss();
            if (Error != null) {
                Toast.makeText(VoiceRecognitionActivity.this, Error, Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(VoiceRecognitionActivity.this, "Source: " + Content, Toast.LENGTH_LONG).show();
            }
        }

    }
}