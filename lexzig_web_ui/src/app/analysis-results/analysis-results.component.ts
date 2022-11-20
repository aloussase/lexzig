import { Component, Input, OnInit } from '@angular/core';
import { json } from '@codemirror/lang-json';
import { EditorState, Extension } from '@codemirror/state';
import { basicSetup, EditorView } from 'codemirror';

@Component({
  selector: 'app-analysis-results',
  templateUrl: './analysis-results.component.html',
  styleUrls: ['./analysis-results.component.scss'],
})
export class AnalysisResultsComponent implements OnInit {
  private _analysisResults: string = '';
  private resultsWindow: EditorView | undefined;

  private editorConfig = (...extensions: Extension[]) => ({
    parent: document.querySelector('#analysis-results')!,
    extensions: [
      ...extensions,
      json(),
      basicSetup,
      EditorView.theme({
        '&': {
          'font-size': '1rem',
          height: '200px',
        },
      }),
    ],
  });

  @Input()
  get analysisResults(): string {
    return this._analysisResults;
  }
  set analysisResults(results: any) {
    this._analysisResults = JSON.stringify(results, null, 2);
    if (this.resultsWindow)
      this.resultsWindow.setState(
        EditorState.create({
          doc: this._analysisResults,
          ...this.editorConfig(),
        })
      );
  }

  constructor() {}

  ngOnInit(): void {
    this.resultsWindow = new EditorView({
      doc: '',
      ...this.editorConfig(),
    });
  }
}
