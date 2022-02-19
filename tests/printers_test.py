from goblincommander.printers import print_title_figure


def test_print_title_figure_prints_only_once(capsys):
    print_title_figure('test')
    captured = capsys.readouterr()
    assert captured.out != ''
    print_title_figure('test')
    captured = capsys.readouterr()
    assert captured.out == ''
