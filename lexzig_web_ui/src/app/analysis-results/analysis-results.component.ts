import { Component, Input, OnInit } from '@angular/core';
import { json } from '@codemirror/lang-json';
import { EditorState, Extension } from '@codemirror/state';
import { basicSetup, EditorView } from 'codemirror';
import { AnalysisSuccess } from '../lexzig-service.service';

@Component({
  selector: 'app-analysis-results',
  templateUrl: './analysis-results.component.html',
  styleUrls: ['./analysis-results.component.scss'],
})
export class AnalysisResultsComponent implements OnInit {
  private ast: string = '';
  private tokens: string = '';
  private astWindow: EditorView | undefined;
  private tokensWindow: EditorView | undefined;

  private editorConfig = (
    idToAttachTo: string,
    ...extensions: Extension[]
  ) => ({
    parent: document.querySelector(idToAttachTo)!,
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
  set analysisResults(results: AnalysisSuccess) {
    if (results === undefined) return;

    this.tokens = JSON.stringify(results.data.tokens, null, 2);
    this.ast = JSON.stringify(results.data.ast, null, 2);

    if (this.astWindow)
      this.astWindow.setState(
        EditorState.create({
          doc: this.ast,
          ...this.editorConfig('#ast'),
        })
      );

    if (this.tokensWindow)
      this.tokensWindow.setState(
        EditorState.create({
          doc: this.tokens,
          ...this.editorConfig('#tokens'),
        })
      );
  }

  constructor() {}

  ngOnInit(): void {
    this.astWindow = new EditorView({
      doc: '',
      ...this.editorConfig('#ast'),
    });

    this.tokensWindow = new EditorView({
      doc: '',
      ...this.editorConfig('#tokens'),
    });
  }
}
