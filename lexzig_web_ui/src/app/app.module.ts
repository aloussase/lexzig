import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { CodeEditorComponent } from './code-editor/code-editor.component';
import { NavbarComponent } from './navbar/navbar.component';
import { AnalysisResultsComponent } from './analysis-results/analysis-results.component';

@NgModule({
  declarations: [
    AppComponent,
    CodeEditorComponent,
    NavbarComponent,
    AnalysisResultsComponent,
  ],
  imports: [BrowserModule, HttpClientModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
