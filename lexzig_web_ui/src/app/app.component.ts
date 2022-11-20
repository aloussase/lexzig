import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'lexzig-ui';

  analysisResults: any;
  analysisError: string | null = null;

  onAnalysedCode({ data }: { data: any }) {
    this.analysisResults = data;
    this.analysisError = null;
  }

  onAnalysisError({ detail }: { detail: string }) {
    this.analysisError = detail;
  }
}
