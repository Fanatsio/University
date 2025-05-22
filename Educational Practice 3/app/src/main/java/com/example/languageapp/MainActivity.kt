package com.example.languageapp

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.speech.RecognizerIntent
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.painter.Painter
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            LanguageApp()
        }
    }
}

@Composable
fun LanguageApp(languageViewModel: LanguageViewModel = viewModel()) {
    var spokenText by remember { mutableStateOf("") }

    val speechRecognitionLauncher = rememberLauncherForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val data: Intent? = result.data
            val texts = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            if (!texts.isNullOrEmpty()) {
                spokenText = texts[0]
                handleSpokenText(spokenText, languageViewModel)
            }
        }
    }

    val backgroundImage: Painter = painterResource(R.drawable.bg)

    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center,
    ) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center,
        ) {
            backgroundImage.let { painter ->
                androidx.compose.foundation.Image(
                    painter = painter,
                    contentDescription = null,
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.FillBounds
                )
            }

            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = "Say the phrase displayed below:\n" +
                            "Hello world!",
                    color = Color.White,
                    style = MaterialTheme.typography.bodyLarge,
                    fontSize = 20.sp,
                    textAlign = TextAlign.Center
                )

                IconButton(
                    onClick = {
                        startSpeechRecognition(speechRecognitionLauncher)
                    },
                ) {
                    Icon(
                        painter = painterResource(id = R.drawable.microphone_icon), // Замените на вашу реальную иконку микрофона
                        contentDescription = "Start Speech Recognition"
                    )
                }

                Text(
                    text = spokenText,
                    modifier = Modifier.align(Alignment.CenterHorizontally)
                )
            }
        }
    }
}

private fun startSpeechRecognition(speechRecognitionLauncher: ActivityResultLauncher<Intent>) {
    val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
    intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
    speechRecognitionLauncher.launch(intent)
}

private fun handleSpokenText(spokenText: String, languageViewModel: LanguageViewModel) {
    // Здесь вызывается функция обработки результата говорения
    // Например, languageViewModel.processSpokenText(spokenText)
}

@Preview(showBackground = true)
@Composable
fun PreviewLanguageApp() {
    LanguageApp()
}
