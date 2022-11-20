import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { basicSetup } from 'codemirror';
import { EditorView, keymap } from '@codemirror/view';
import { rust } from '@codemirror/lang-rust';
import { indentWithTab } from '@codemirror/commands';
import { LexzigService } from '../lexzig-service.service';

@Component({
  selector: 'app-code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls: ['./code-editor.component.scss'],
})
export class CodeEditorComponent implements OnInit {
  private editor: EditorView | null = null;

  showCopiedAlert = false;

  @Output() analysedCode = new EventEmitter<{ data: any }>();
  @Output() analysisError = new EventEmitter<{ detail: string }>();

  constructor(private lexzigService: LexzigService) {}

  ngOnInit(): void {
    this.editor = this.createEditor();
  }

  onRun() {
    const code = this.editor?.state.doc.toString();
    if (!code) return;

    this.lexzigService.analyseCode(code).subscribe((response) => {
      if ('data' in response) {
        this.analysedCode.emit(response);
      } else {
        this.analysisError.emit(response);
      }
    });
  }

  /**
   * Copy the code from the editor to the clipboard.
   */
  onCopy() {
    if (this.editor) {
      navigator.clipboard.writeText(this.editor.state.doc.toString());
      this.showCopiedAlert = true;
      setTimeout(() => (this.showCopiedAlert = false), 2000);
    }
  }

  private static sampleCode = `\
const Circle = struct {
  x: i32, 
  y: i32,

  pub fn new(x: i32, y: i32) Circle {
    return Circle{
      .x = x,
      .y = y,
    };
  }
};
`;

  private createEditor(): EditorView {
    return new EditorView({
      doc: CodeEditorComponent.sampleCode,
      parent: document.querySelector('#editor')!,
      extensions: [
        basicSetup,
        keymap.of([indentWithTab]),
        rust(), // Forgive me father, for I have sinned...
        EditorView.theme({
          '&': {
            'font-size': '1.2rem',
            height: '300px',
          },
        }),
      ],
    });
  }
}
